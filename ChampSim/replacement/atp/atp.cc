#include <algorithm>
#include <map>
#include <utility>
#include <string>
#include <vector>
#include <deque> // For tracking recent accesses
#include <iostream>
#include <cstdlib> // For getenv, abort
#include <cassert> // For assert
#include <cmath>   // For std::ceil
#include <limits>  // For std::numeric_limits
#include <stdexcept> // For std::invalid_argument, std::out_of_range

#include "cache.h" // Includes definition for CACHE and BLOCK
#include "util.h"  // May contain utility functions
#include "vmem.h"  // Needed for vmem->STLB_MISS_RATE in commented sections

// ============================================================================
// === Global Data Structures for Policies & Switching (Keyed by CACHE*) ===
// ============================================================================

// --- Dynamic Policy Switching State ---
namespace dynamic_policy {
    // Constants for switching logic
    const size_t ACCESS_HISTORY_WINDOW = 100000; // Look at last 100k accesses
    const uint64_t SWITCH_CHECK_INTERVAL = 1000; // Check policy every 1k accesses

    // Maps keyed by CACHE* to store state for each cache instance
    std::map<CACHE*, std::string> active_policy_name;        // Current policy ("itp", "dtp", "srrip")
    std::map<CACHE*, std::deque<bool>> recent_access_types; // History: true=instruction, false=data
    std::map<CACHE*, size_t> instruction_access_count;      // Count of instructions in the history window
    std::map<CACHE*, uint64_t> access_counter_for_switch_check; // Counter to trigger checks

    // --- Helper function to update policy based on history ---
    void update_policy_choice(CACHE* self) {
        // Check if maps contain entries for 'self' and if history is non-empty
        if (!recent_access_types.count(self) || recent_access_types[self].empty()) {
            return; // No history yet for this cache instance
        }

        // Calculate instruction access percentage
        double instr_percentage = (static_cast<double>(instruction_access_count[self]) * 100.0) / static_cast<double>(recent_access_types[self].size());

        std::string previous_policy = active_policy_name[self];
        std::string next_policy;

        // Determine next policy based on thresholds
        if (instr_percentage >= 50.0) {
            next_policy = "itp";
        } else if (instr_percentage >= 30.0) { // 30% <= instr < 50%
            next_policy = "srrip";
        } else { // instr < 30%
            next_policy = "dtp";
        }

        // Update policy if it changed
        if (next_policy != previous_policy) {
            active_policy_name[self] = next_policy;
            // Optional: Print a message indicating the policy switch
            // std::cout << self->NAME << " Cycle: " << self->current_cycle << " Accesses: " << recent_access_types[self].size()
            //           << " Instr%: " << std::fixed << std::setprecision(2) << instr_percentage
            //           << " Switching policy from " << previous_policy << " to " << active_policy_name[self] << std::endl;
        }
    }
} // namespace dynamic_policy


// ============================================================================
// === iTP Policy Implementation (Instruction Translation Prioritization) ===
// ============================================================================
namespace itp_policy {

    // Internal helper class for saturating counter
    class SatCnt {
        private: uint32_t cnt = 0; uint32_t max_value;
        public: SatCnt(uint32_t nbits = 3) { max_value = 50; } // Default nbits unused, max hardcoded
        SatCnt operator++(int) { SatCnt tmp = *this; if (cnt < max_value) cnt++; return tmp; }
        void reset() { cnt = 0; }
        bool saturated() { return (cnt == max_value); }
    };

    // Policy parameters with default values
    uint32_t instr_pos = 4, data_pos = 8; uint32_t maxRRPV = 12;

    // Global frequency tracking for instruction VPNs
    std::map<uint64_t, int32_t> vpn_freq_acc;

    // Per-cache instance data structures, keyed by CACHE*
    std::map<CACHE*, std::vector<uint32_t>> least_recently_used; // RRPV values
    std::map<CACHE*, std::vector<SatCnt>> freq_cnt;             // Local block frequency counters

    // Initialization logic for a specific cache instance
    void initialize(CACHE* self, uint32_t sets, uint32_t ways) {
        const char* max_lru_env = getenv("ITP_MAX_LRU");
        const char* instr_pos_env = getenv("ITP_INSTR_POS");
        const char* data_pos_env = getenv("ITP_DATA_POS");
        try { // Read parameters from environment or use defaults
            if (max_lru_env) maxRRPV = std::stoi(max_lru_env);
            if (instr_pos_env) instr_pos = std::stoi(instr_pos_env);
            if (data_pos_env) data_pos = std::stoi(data_pos_env);
        } catch (const std::exception& e) {
            std::cerr << "WARNING: Invalid iTP environment variable for " << self->NAME << ": " << e.what() << ". Using defaults." << std::endl;
        }

        std::cout << self->NAME << " initializing iTP with max lru@" << maxRRPV
                  << ", instr@" << instr_pos << ", data@" << data_pos << std::endl;

        uint64_t total_blocks = static_cast<uint64_t>(sets) * ways;
        least_recently_used[self].assign(total_blocks, maxRRPV - 1); // Initialize RRPV near eviction
        freq_cnt[self].assign(total_blocks, SatCnt()); // Initialize local counters
    }

    // Update state logic for a specific cache instance
    void update_state(CACHE* self, uint32_t set, uint32_t way,
                       uint64_t victim_addr, uint32_t type, uint8_t hit, bool is_instr) { // Use bool is_instr
        uint64_t block_index = static_cast<uint64_t>(set) * self->NUM_WAY + way;
        // Basic bounds check
        if (!least_recently_used.count(self) || block_index >= least_recently_used[self].size()) { assert(false); return; }

        if (!is_instr) { // --- Data Access ---
            least_recently_used[self][block_index] = hit ? (maxRRPV - data_pos) : (maxRRPV - 1);
            return;
        }

        // --- Instruction Access ---
        uint64_t vpn = victim_addr >> LOG2_PAGE_SIZE;
        // Get or insert frequency count (starts at 0)
        int32_t acc_freq = vpn_freq_acc.try_emplace(vpn, 0).first->second;

        // Set RRPV based on global frequency
        least_recently_used[self][block_index] = (acc_freq < 50) ? (maxRRPV - instr_pos) : 0;

        // Increment global frequency count safely
        if (vpn_freq_acc[vpn] < std::numeric_limits<int32_t>::max()) vpn_freq_acc[vpn]++;

        // Update local block frequency counter
        if (!freq_cnt.count(self) || block_index >= freq_cnt[self].size()) { assert(false); return; } // Bounds check
        if (!hit) freq_cnt[self][block_index].reset(); else freq_cnt[self][block_index]++;
    }

    // Victim finding logic for a specific cache instance
    uint32_t find_victim(CACHE* self, uint32_t set) {
        if (!least_recently_used.count(self)) { assert(false); return 0; } // Check if map entry exists

        auto vec_begin = std::begin(least_recently_used[self]);
        auto begin = std::next(vec_begin, static_cast<long long>(set) * self->NUM_WAY);
        auto end = std::next(begin, self->NUM_WAY);

        // Ensure iterators are valid
        if (begin < vec_begin || end > std::end(least_recently_used[self])) {assert(false); return 0;}

        auto victim = std::find_if(begin, end, [](uint32_t x) { return x == maxRRPV; });
        while (victim == end) {
            bool changed = false;
            for (auto it = begin; it != end; ++it) {
                 if (*it < maxRRPV) {
                     (*it)++;
                     changed = true;
                 }
            }
             if (!changed) { // Should not happen with maxRRPV > 0
                  assert(false);
                  return 0; // Prevent infinite loop, return way 0
             }
            victim = std::find_if(begin, end, [](uint32_t x) { return x == maxRRPV; });
        }
        return static_cast<uint32_t>(std::distance(begin, victim));
    }

    // Final stats function (optional)
    void final_stats(CACHE* self) { /* Can print policy-specific stats here */ }

} // namespace itp_policy


// ============================================================================
// === DTP Policy Implementation (Data Translation Prioritization) ===
// ============================================================================
namespace dtp_policy {

    // Policy parameters with default values
    uint32_t instr_pos_dtp = 8, data_pos_dtp = 4; uint32_t maxRRPV_dtp = 12;

    // Per-cache instance data structures
    std::map<CACHE*, std::vector<uint32_t>> least_recently_used_dtp; // RRPV values per cache

    // Initialization logic
    void initialize(CACHE* self, uint32_t sets, uint32_t ways) {
        const char* max_lru_env = getenv("DTP_MAX_LRU");
        const char* instr_pos_env = getenv("DTP_INSTR_POS");
        const char* data_pos_env = getenv("DTP_DATA_POS");
        try { // Read parameters or use defaults
            if (max_lru_env) maxRRPV_dtp = std::stoi(max_lru_env);
            if (instr_pos_env) instr_pos_dtp = std::stoi(instr_pos_env);
            if (data_pos_env) data_pos_dtp = std::stoi(data_pos_env);
        } catch (const std::exception& e) {
            std::cerr << "WARNING: Invalid DTP environment variable for " << self->NAME << ": " << e.what() << ". Using defaults." << std::endl;
        }

        std::cout << self->NAME << " initializing DTP with max lru@" << maxRRPV_dtp
                  << ", instr@" << instr_pos_dtp << ", data@" << data_pos_dtp << std::endl;

        uint64_t total_blocks = static_cast<uint64_t>(sets) * ways;
        least_recently_used_dtp[self].assign(total_blocks, maxRRPV_dtp - 1); // Initialize RRPV near eviction
    }

    // Update state logic
    void update_state(CACHE* self, uint32_t set, uint32_t way,
                       uint64_t victim_addr, uint32_t type, uint8_t hit, bool is_instr) { // Use bool is_instr
        uint64_t block_index = static_cast<uint64_t>(set) * self->NUM_WAY + way;
        if (!least_recently_used_dtp.count(self) || block_index >= least_recently_used_dtp[self].size()) { assert(false); return; }

        if (is_instr) { // --- Instruction Access (LOW Priority) ---
            least_recently_used_dtp[self][block_index] = hit ? (maxRRPV_dtp - instr_pos_dtp) : (maxRRPV_dtp - 1);
            return;
        }

        // --- Data Access (HIGH Priority) ---
        // Simple DTP sets a high priority (low RRPV) regardless of hit/miss or frequency
        least_recently_used_dtp[self][block_index] = maxRRPV_dtp - data_pos_dtp;
        // Alternative: Set to highest priority (0) on hit/fill
        // least_recently_used_dtp[self][block_index] = 0;
    }

    // Victim finding logic
    uint32_t find_victim(CACHE* self, uint32_t set) {
         if (!least_recently_used_dtp.count(self)) { assert(false); return 0; } // Check map entry

        auto vec_begin = std::begin(least_recently_used_dtp[self]);
        auto begin = std::next(vec_begin, static_cast<long long>(set) * self->NUM_WAY);
        auto end = std::next(begin, self->NUM_WAY);

        if (begin < vec_begin || end > std::end(least_recently_used_dtp[self])) { assert(false); return 0;} // Bounds check

        auto victim = std::find_if(begin, end, [](uint32_t x) { return x == maxRRPV_dtp; });
        while (victim == end) {
            bool changed = false;
            for (auto it = begin; it != end; ++it) {
                 if (*it < maxRRPV_dtp) {
                    (*it)++;
                    changed = true;
                 }
            }
            if (!changed) { assert(false); return 0; } // Prevent infinite loop
            victim = std::find_if(begin, end, [](uint32_t x) { return x == maxRRPV_dtp; });
        }
        return static_cast<uint32_t>(std::distance(begin, victim));
    }

    // Final stats function (optional)
    void final_stats(CACHE* self) { /* Empty */ }

} // namespace dtp_policy


// ============================================================================
// === SRRIP Policy Implementation (Placeholder) ===
// ============================================================================
namespace srrip_policy {

    // Policy parameters with default values
    uint32_t maxRRPV_srrip = 3; // Default SRRIP max RRPV (often 2^M - 1, e.g., M=2 bits -> max=3)

    // Per-cache instance data structures
    std::map<CACHE*, std::vector<uint32_t>> rrpv_values; // RRPV values per cache

    // Initialization logic
    void initialize(CACHE* self, uint32_t sets, uint32_t ways) {
        const char* max_rrpv_env = getenv("SRRIP_MAX_RRPV");
        try { // Read parameter or use default
            if (max_rrpv_env) maxRRPV_srrip = std::stoi(max_rrpv_env);
        } catch (const std::exception& e) {
             std::cerr << "WARNING: Invalid SRRIP environment variable for " << self->NAME << ": " << e.what() << ". Using default." << std::endl;
        }

        std::cout << self->NAME << " initializing SRRIP placeholder with max RRPV@" << maxRRPV_srrip << std::endl;
        uint64_t total_blocks = static_cast<uint64_t>(sets) * ways;
        // Initialize SRRIP RRPV. Often initialized to maxRRPV or maxRRPV-1. Using maxRRPV here.
        rrpv_values[self].assign(total_blocks, maxRRPV_srrip);
    }

    // Update state logic (Placeholder)
    void update_state(CACHE* self, uint32_t set, uint32_t way,
                       uint64_t victim_addr, uint32_t type, uint8_t hit, bool is_instr) { // Use bool is_instr
        uint64_t block_index = static_cast<uint64_t>(set) * self->NUM_WAY + way;
        if (!rrpv_values.count(self) || block_index >= rrpv_values[self].size()) { assert(false); return; }

        // Basic SRRIP: Set RRPV to 0 on hit
        if (hit) {
            rrpv_values[self][block_index] = 0;
        }
        // On a miss (fill), the RRPV is typically set *after* the victim is chosen
        // (usually to maxRRPV_srrip - 1), handled in CACHE::find_victim.
    }

    // Victim finding logic (Placeholder)
    uint32_t find_victim(CACHE* self, uint32_t set) {
        if (!rrpv_values.count(self)) { assert(false); return 0; } // Check map entry

        auto vec_begin = std::begin(rrpv_values[self]);
        auto begin = std::next(vec_begin, static_cast<long long>(set) * self->NUM_WAY);
        auto end = std::next(begin, self->NUM_WAY);

        if (begin < vec_begin || end > std::end(rrpv_values[self])) { assert(false); return 0;} // Bounds check

        // Find first block with RRPV == maxRRPV_srrip
        auto victim = std::find_if(begin, end, [](uint32_t x){ return x == maxRRPV_srrip; });
        // AGING loop: If none found, increment all RRPVs until one reaches maxRRPV_srrip
        while (victim == end) {
            bool changed = false;
            for(auto it=begin; it!=end; ++it) {
                 if (*it < maxRRPV_srrip) {
                      (*it)++;
                      changed = true;
                 }
            }
             if (!changed) { assert(false); return 0; } // Prevent infinite loop
            victim = std::find_if(begin, end, [](uint32_t x){ return x == maxRRPV_srrip; });
        }
        return static_cast<uint32_t>(std::distance(begin, victim));
    }

    // Final stats function (optional)
    void final_stats(CACHE* self) { /* Empty */ }

} // namespace srrip_policy


// ============================================================================
// === CACHE Class Method Implementations (Using Dynamic Policy Switching) ===
// ============================================================================

// Initialize replacement policy state and dynamic switching mechanism
void CACHE::initialize_replacement()
{
    // Initialize data structures for ALL potential policies for this cache instance
    itp_policy::initialize(this, NUM_SET, NUM_WAY);
    dtp_policy::initialize(this, NUM_SET, NUM_WAY);
    srrip_policy::initialize(this, NUM_SET, NUM_WAY);

    // Initialize dynamic switching state for this cache instance in global maps
    dynamic_policy::recent_access_types[this].clear();
    dynamic_policy::instruction_access_count[this] = 0;
    dynamic_policy::access_counter_for_switch_check[this] = 0;
    dynamic_policy::active_policy_name[this] = "srrip"; // Default starting policy

    std::cout << NAME << " initialized dynamic policy switching (iTP/DTP/SRRIP). Starting with: " << dynamic_policy::active_policy_name[this] << std::endl;
}

// Update replacement state based on access, manage history, and switch policy if needed
void CACHE::update_replacement_state(uint32_t triggering_cpu, uint32_t set, uint32_t way,
                                     uint64_t full_addr, uint64_t ip, uint64_t victim_addr,
                                     uint32_t type, uint8_t hit, CACHE::REP_POL_XARGS xargs)
{
    // Extract the boolean instruction flag from the private struct
    bool is_instr = xargs.is_instr;

    // --- Update Access History for Dynamic Switching ---
    // Ensure map entries exist before accessing
    dynamic_policy::recent_access_types.try_emplace(this);
    dynamic_policy::instruction_access_count.try_emplace(this, 0);
    dynamic_policy::access_counter_for_switch_check.try_emplace(this, 0);
    dynamic_policy::active_policy_name.try_emplace(this, "srrip"); // Ensure policy name exists

    dynamic_policy::recent_access_types[this].push_back(is_instr);
    if (is_instr) {
        dynamic_policy::instruction_access_count[this]++;
    }

    // Maintain the sliding window of access history
    if (dynamic_policy::recent_access_types[this].size() > dynamic_policy::ACCESS_HISTORY_WINDOW) {
        bool oldest_is_instr = dynamic_policy::recent_access_types[this].front();
        dynamic_policy::recent_access_types[this].pop_front();
        if (oldest_is_instr) {
            // Prevent underflow if count somehow became zero unexpectedly
            if (dynamic_policy::instruction_access_count[this] > 0) {
                 dynamic_policy::instruction_access_count[this]--;
            }
        }
    }

    // --- Check if it's time to re-evaluate the active policy ---
    dynamic_policy::access_counter_for_switch_check[this]++;
    if (dynamic_policy::access_counter_for_switch_check[this] >= dynamic_policy::SWITCH_CHECK_INTERVAL) {
        dynamic_policy::update_policy_choice(this); // Update active_policy_name[this]
        dynamic_policy::access_counter_for_switch_check[this] = 0; // Reset check counter
    }

    // --- Dispatch to the currently active policy's update function ---
    const std::string& current_policy = dynamic_policy::active_policy_name[this];
    if (current_policy == "itp") {
        itp_policy::update_state(this, set, way, victim_addr, type, hit, is_instr);
    } else if (current_policy == "dtp") {
        dtp_policy::update_state(this, set, way, victim_addr, type, hit, is_instr);
    } else if (current_policy == "srrip") {
        srrip_policy::update_state(this, set, way, victim_addr, type, hit, is_instr);
    } else {
        // Should not happen if initialized correctly
        std::cerr << "ERROR: Unknown policy in update_replacement_state: " << current_policy << " for " << NAME << std::endl;
    }
}

// Find victim based on the currently active policy
uint32_t CACHE::find_victim(uint32_t triggering_cpu, uint64_t instr_id, uint32_t set, const BLOCK* current_set, uint64_t ip, uint64_t full_addr, uint32_t type)
{
    // Ensure map entry exists, defaulting to srrip if somehow missing after init
    const std::string& current_policy = dynamic_policy::active_policy_name.try_emplace(this, "srrip").first->second;
    uint32_t victim_way = 0; // Default victim way

    // --- Dispatch to the currently active policy's find_victim function ---
    if (current_policy == "itp") {
        victim_way = itp_policy::find_victim(this, set);
    } else if (current_policy == "d
