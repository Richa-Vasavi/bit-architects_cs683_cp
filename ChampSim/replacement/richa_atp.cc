#include <algorithm>
#include <map>
#include <utility>
#include <string>
#include <cassert>
#include <iostream>

#include "cache.h"
#include "util.h"

//#define maxRRPV 12
//#define NUM_POLICY 2
//#define SDM_SIZE 32
//#define TOTAL_SDM_SETS NUM_CPUS* NUM_POLICY* SDM_SIZE
//#define BIP_MAX 32
//#define PSEL_WIDTH 10
//#define PSEL_MAX ((1 << PSEL_WIDTH) - 1)
//#define PSEL_THRS PSEL_MAX / 2

//#std::map<CACHE*, unsigned> bip_counter;
//#std::map<CACHE*, std::vector<std::size_t>> rand_sets;
//#std::map<std::pair<CACHE*, std::size_t>, unsigned> PSEL;

uint32_t instr_pos, data_pos;
uint32_t maxRRPV;

std::map<uint64_t, int32_t> vpn_freq_acc;

namespace {
  // ------------------------------
  // Saturating Counter
  // ------------------------------
  class SatCnt {
    private:
      uint32_t cnt;        // current counter value
      uint32_t max_value;  // max value

    public:
      SatCnt(uint32_t nbits) {
        // keep behavior of forcing max to 50
        max_value = 1u << nbits;
        max_value = 50;
        cnt = 0; // initialize to avoid UB before first use
        std::cout << "Init sat counter with " << nbits
                  << " bits (max:" << max_value  << ")." << std::endl;
      }

      SatCnt operator++(int) {
        SatCnt tmp = *this;           // postfix returns old value
        if (cnt < max_value) cnt++;   // saturate at max
        return tmp;
      }

      void reset() { cnt = 0; }

      bool saturated() { return (cnt == max_value); }
  };

  // ------------------------------
  // Tunables
  // ------------------------------
  constexpr uint64_t TRAINING_ACCESSES = 200'000;
  constexpr int32_t  PSEL_MIN = 0;
  constexpr int32_t  PSEL_MAX = 100;
  constexpr int32_t  PSEL_START = 50;
  constexpr int32_t  PSEL_ITP_THRESHOLD_LOW  = 60; // 60..100 -> iTP
  constexpr int32_t  PSEL_DTP_THRESHOLD_HIGH = 40; // 0..40   -> dTP

  // ------------------------------
  // Per-cache state
  // ------------------------------
  uint32_t TLB_LOWER_STRESS_THRESHOLD;
  uint32_t TLB_UPPER_STRESS_THRESHOLD;

  // Per cache metadata arrays
  std::map<CACHE*, std::vector<uint64_t>> last_used_cycles;     // optional time-based LRU
  std::map<CACHE*, std::vector<uint32_t>> least_recently_used;  // stores RRPV per line
  std::map<CACHE*, std::vector<SatCnt>>   freq_cnt;             // per-line frequency counters

  // Per cache policy selector and access counters
  std::map<CACHE*, uint64_t> access_count_map;
  std::map<CACHE*, int32_t>  psel_map;

  // ------------------------------
  // Small helpers
  // ------------------------------
  inline int32_t clamp_psel(int32_t v) {
    if (v < PSEL_MIN) return PSEL_MIN;
    if (v > PSEL_MAX) return PSEL_MAX;
    return v;
  }

  inline uint32_t index_of(CACHE* self, uint32_t set, uint32_t way) {
    return set * self->NUM_WAY + way;
  }

  // ------------------------------
  // Policy Implementations
  // ------------------------------

  // SRRIP:
  // - On hit:   set RRPV = 0 (very recently used)
  // - On fill:  insert at RRPV = maxRRPV - 1 (long re-reference interval)
  void do_SRRIP(CACHE* self, uint32_t set, uint32_t way, uint8_t hit) {
    auto& rrpv = ::least_recently_used[self];
    const auto idx = index_of(self, set, way);

    if (hit) {
      rrpv[idx] = 0;
    } else {
      rrpv[idx] = (maxRRPV > 0) ? (maxRRPV - 1) : 0;
    }
  }

  // Your original iTP logic (instruction-priority) preserved:
  // - For DATA:
  //     on hit:  RRPV = maxRRPV - data_pos
  //     on miss: RRPV = maxRRPV - 1
  // - For INSTR (fac-based):
  //     acc_freq from vpn; if < 50 → insert at maxRRPV - instr_pos
  //     else insert at RRPV=0
  //     update vpn_freq_acc; freq_cnt reset/++
  void do_iTP(CACHE* self,
              uint32_t set, uint32_t way,
              uint8_t hit, uint32_t /*type*/,
              bool is_instr, uint64_t victim_addr)
  {
    auto& rrpv = ::least_recently_used[self];
    const auto idx = index_of(self, set, way);

    if (!is_instr) {
      // DATA path (as in your code)
      if (hit) {
        rrpv[idx] = maxRRPV - data_pos;
        return;
      }
      rrpv[idx] = (maxRRPV > 0) ? (maxRRPV - 1) : 0;
      return;
    }

    // INSTR path (idip_fac logic)
    uint64_t vpn = victim_addr >> LOG2_PAGE_SIZE;

    int32_t acc_freq = 0;
    if (vpn_freq_acc.find(vpn) == vpn_freq_acc.end()) {
      acc_freq = -2;
      vpn_freq_acc[vpn] = -2;
    } else {
      acc_freq = vpn_freq_acc[vpn];
    }

    if (acc_freq < 50) {
      rrpv[idx] = maxRRPV - instr_pos;
    } else {
      rrpv[idx] = 0;
    }

    vpn_freq_acc[vpn]++;

    if (!hit) {
      ::freq_cnt[self][idx].reset();
    } else {
      ::freq_cnt[self][idx]++;
    }
  }

  // dTP (data-priority): mirror iTP but prioritizes DATA instead.
  // - For DATA (mirrors iTP's INSTR path):
  //     acc_freq from vpn; if < 50 → insert at maxRRPV - data_pos
  //     else insert at RRPV=0
  //     update vpn_freq_acc; freq_cnt reset/++
  // - For INSTR (mirrors iTP's DATA path):
  //     on hit:  RRPV = maxRRPV - instr_pos
  //     on miss: RRPV = maxRRPV - 1
  void do_dTP(CACHE* self,
              uint32_t set, uint32_t way,
              uint8_t hit, uint32_t /*type*/,
              bool is_instr, uint64_t victim_addr)
  {
    auto& rrpv = ::least_recently_used[self];
    const auto idx = index_of(self, set, way);

    if (!is_instr) {
      // DATA path (mirror of iTP's INSTR path)
      uint64_t vpn = victim_addr >> LOG2_PAGE_SIZE;

      int32_t acc_freq = 0;
      if (vpn_freq_acc.find(vpn) == vpn_freq_acc.end()) {
        acc_freq = -2;
        vpn_freq_acc[vpn] = -2;
      } else {
        acc_freq = vpn_freq_acc[vpn];
      }

      if (acc_freq < 50) {
        rrpv[idx] = maxRRPV - data_pos;
      } else {
        rrpv[idx] = 0;
      }

      vpn_freq_acc[vpn]++;

      if (!hit) {
        ::freq_cnt[self][idx].reset();
      } else {
        ::freq_cnt[self][idx]++;
      }
      return;
    }

    // INSTR path (mirror of iTP's DATA path)
    if (hit) {
      rrpv[idx] = maxRRPV - instr_pos;
      return;
    }
    rrpv[idx] = (maxRRPV > 0) ? (maxRRPV - 1) : 0;
  }

} // anonymous namespace

// ------------------------------
// CACHE methods
// ------------------------------
void CACHE::initialize_replacement()
{
  if (getenv("TLB_LOWER_STRESS_THRESHOLD")) {
    ::TLB_LOWER_STRESS_THRESHOLD = std::stoi(getenv("TLB_LOWER_STRESS_THRESHOLD"));
  }

  if (getenv("TLB_UPPER_STRESS_THRESHOLD")) {
    ::TLB_UPPER_STRESS_THRESHOLD = std::stoi(getenv("TLB_UPPER_STRESS_THRESHOLD"));
    ::TLB_UPPER_STRESS_THRESHOLD = 2.5; // NOTE: uint32_t truncates to 2 if kept as uint32_t
  }

  // REQUIRED environment variables (ensure they are set before run)
  maxRRPV   = std::stoi(getenv("ITP_MAX_LRU"));
  instr_pos = std::stoi(getenv("ITP_INSTR_POS"));
  data_pos  = std::stoi(getenv("ITP_DATA_POS"));

  std::cout << this->NAME << " using iTP with max lru@" << maxRRPV << std::endl;
  std::cout << this->NAME << " using iTP with instr@" << instr_pos
            << " and data@" << data_pos << std::endl;

  // allocate per-line arrays using per-cache geometry
  ::last_used_cycles[this]     = std::vector<uint64_t>(this->NUM_SET * this->NUM_WAY);
  ::least_recently_used[this]  = std::vector<uint32_t>(this->NUM_SET * this->NUM_WAY);
  ::freq_cnt[this]             = std::vector<SatCnt>(this->NUM_SET * this->NUM_WAY, SatCnt(3));

  // Initialize per-cache PSEL and access counters
  ::access_count_map[this] = 0;
  ::psel_map[this] = PSEL_START;
}

// called on every cache hit and cache fill
void CACHE::update_replacement_state(uint32_t triggering_cpu, uint32_t set, uint32_t way,
                                     uint64_t full_addr, uint64_t ip, uint64_t victim_addr,
                                     uint32_t type, uint8_t hit,
                                     CACHE::REP_POL_XARGS xargs)
{
  // --- Update per-cache access count
  auto& access_count = ::access_count_map[this];
  auto& psel         = ::psel_map[this];
  access_count++;

  // --- Update PSEL by access type
  if (xargs.is_instr) psel++;
  else                psel--;

  psel = clamp_psel(psel);

  // TRAINING PHASE: first 200k accesses use SRRIP (counter still updated above)
  if (access_count <= TRAINING_ACCESSES) {
    do_SRRIP(this, set, way, hit);
    return;
  }

  // ADAPTIVE PHASE: choose policy by PSEL
  if (psel <= PSEL_DTP_THRESHOLD_HIGH) {
    // 0..40 -> dTP
    do_dTP(this, set, way, hit, type, xargs.is_instr, victim_addr);
  } else if (psel >= PSEL_ITP_THRESHOLD_LOW) {
    // 60..100 -> iTP
    do_iTP(this, set, way, hit, type, xargs.is_instr, victim_addr);
  } else {
    // 40..60 -> SRRIP
    do_SRRIP(this, set, way, hit);
  }

  return;
}

// find replacement victim
uint32_t CACHE::find_victim(uint32_t triggering_cpu, uint64_t instr_id, uint32_t set,
                            const BLOCK* current_set, uint64_t ip, uint64_t full_addr, uint32_t type)
{
  // Optional LRU-by-time mode (disabled)
  /*
  if (((vmem->STLB_MISS_RATE >= ::TLB_LOWER_STRESS_THRESHOLD) &&
       (vmem->STLB_MISS_RATE <= ::TLB_UPPER_STRESS_THRESHOLD)) && false) {
    auto begin = std::next(std::begin(::last_used_cycles[this]), set * this->NUM_WAY);
    auto end   = std::next(begin, this->NUM_WAY);
    auto victim = std::min_element(begin, end);
    assert(begin <= victim);
    assert(victim < end);
    return static_cast<uint32_t>(std::distance(begin, victim));
  }
  */

  // Look for a line with RRPV == maxRRPV
  auto begin  = std::next(std::begin(::least_recently_used[this]), set * this->NUM_WAY);
  auto end    = std::next(begin, this->NUM_WAY);
  auto victim = std::find_if(begin, end, [](uint32_t x) { return x == maxRRPV; }); // hijack the lru field

  while (victim == end) {
    for (auto it = begin; it != end; ++it)
      (*it)++;

    victim = std::find_if(begin, end, [](uint32_t x) { return x == maxRRPV; });
  }

  return static_cast<uint32_t>(std::distance(begin, victim));
}

bool cmp(const std::pair<uint64_t, uint32_t> &a, const std::pair<uint64_t, uint32_t> &b)
{
  return (a.second < b.second);
}

// use this function to print out your own stats at the end of simulation
void CACHE::replacement_final_stats() {
  /*
  std::vector <std::pair<uint64_t, uint32_t>> sorted_fac;
  for (auto& i : vpn_freq_acc) {
    sorted_fac.push_back(i);
  }
  std::sort(sorted_fac.begin(), sorted_fac.end(), cmp);
  for (auto& i : sorted_fac) {
    std::cout << std::hex << i.first << std::dec;
    std::cout << ", " << i.second + maxRRPV + 1 << std::endl;
  }
  */
}

