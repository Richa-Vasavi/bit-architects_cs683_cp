<p align="center">
  <h1 align="center"> ChampSim </h1>
  <p> ChampSim is a trace-based simulator for a microarchitecture study. You can sign up to the public mailing list by sending an empty mail to champsim+subscribe@googlegroups.com. If you have questions about how to use ChampSim, you can often receive a quicker response on the mailing list. Please reserve GitHub Issues for bugs. <p>
</p>

# Using ChampSim

ChampSim is the result of academic research. To support its continued growth, please cite our work when you publish results that use ChampSim by clicking "Cite this Repository" in the sidebar.

# Compile

ChampSim takes a JSON configuration script. Examine `champsim_config.json` for a fully-specified example. All options described in this file are optional and will be replaced with defaults if not specified. The configuration scrip can also be run without input, in which case an empty file is assumed.
```
$ ./config.sh <configuration file>
$ make
$ source set_env.sh
```

Traces used: https://drive.google.com/drive/folders/1KHC3VXy-mOTc1qvIrVmEkwYMG1tK62DX?usp=sharing

# Run simulation

Execute the binary directly.
```
$ bin/champsim --warmup_instructions 200000000 --simulation_instructions 500000000 ~/path/to/traces/smt_srv540_ap_srv495_ap_1024i.champsimtrace.xz
```

The number of warmup and simulation instructions given will be the number of instructions retired. Note that the statistics printed at the end of the simulation include only the simulation phase.

# How to change the replacement policy and other values related to memory
open champsim_fdip_baseline.json and change accordingly to observe required changes


# Project README: Evaluation of STLB Replacement Policies (LRU, SRRIP, iTP, ATP)

## Project Overview

This project investigates the performance impact of various replacement policies on the **Second-Level Translation Lookaside Buffer (STLB)** using the **ChampSim simulation framework**. Building upon the **Instruction Translation Prioritization (iTP)** policy from the ASPLOS '25 paper "Instruction-Aware Cooperative TLB and Cache Replacement Policies", we implemented and evaluated several configurations:

1.  **Baseline LRU:** Standard Least Recently Used policy for all cache/TLB levels.
2.  **SRRIP:** Static Re-Reference Interval Prediction policy for the STLB.
3.  **iTP:** The instruction-prioritizing policy from the paper applied to the STLB.
4.  **ATP (Adaptive Translation Policy):** A novel dynamic policy developed for this project that switches the STLB replacement strategy between iTP, DTP (Data Translation Prioritization), and SRRIP based on the ratio of instruction vs. data accesses observed in a recent history window.

We also explored the impact of STLB configuration, comparing results primarily using a **128-set, 12-way STLB** (1536 entries, matching the paper's configuration) and potentially other configurations like a 64-set STLB.

## Artifact Base

* We utilized the official artifact for the ASPLOS '25 paper.
* The baseline hardware configuration corresponds to `champsim_fdip_baseline.json`, including active L1/L2 prefetchers.

## Code Modifications

1.  **Policy Implementations:**
    * The original `itp.cc` logic was adapted.
    * New logic for DTP and a placeholder SRRIP were implemented.
    * These were structured within namespaces (`itp_policy`, `dtp_policy`, `srrip_policy`) in a single file (e.g., `replacement_policies.cc` or `atp.cc`) to manage policy state globally using `std::map` keyed by `CACHE*` pointers, avoiding modifications to `cache.h`.

2.  **Dynamic Policy Switching (ATP):**
    * Logic added to `CACHE::update_replacement_state` tracks the last 100,000 STLB access types.
    * Every 1,000 accesses, the instruction access percentage is calculated.
    * The active policy for the STLB is switched based on this percentage:
        * 0% - <30% Instruction Accesses: **DTP**
        * 30% - <50% Instruction Accesses: **SRRIP**
        * 50% - 100% Instruction Accesses: **iTP**
    * `CACHE` methods dispatch calls to the active policy's functions.

3.  **Enhanced Statistics Output:**
    * `src/plain_printer.cc` and `inc/stats_printer.h` were modified to include **MPKI** for all relevant levels and improve output formatting.
    * Bash scripts were enhanced to extract additional metrics like detailed access counts (`iACCESS`, `dACCESS`, etc.).

## Experiment Setup & Execution

1.  **Changing Policies:**
    * For **static policies** (LRU, SRRIP, iTP): Modify the `champsim_fdip_baseline.json` file. Find the `"STLB"` block and change the `"replacement": "..."` value to `"lru"`, `"srrip"`, or `"itp"`. Recompile after changing the JSON using `./config.sh champsim_fdip_baseline.json` and `make`.
    * For the **dynamic ATP policy:** Compile the code containing the switching logic (e.g., `atp.cc`). The policy switching is handled internally based on access history. Ensure necessary environment variables for all sub-policies (ITP, DTP, SRRIP parameters) are set via `set_env.sh`.

2.  **Running Simulations:**
    * **Environment:** Navigate to the `ChampSim` directory (e.g., `.../128set/ChampSim`). Source the environment script: `source set_env.sh`. This sets required variables for statistics output and policy parameters.
    * **Execution:** Run the simulation script: `./run.sh`. This script iterates through trace files (expected in a directory like `../traces` relative to the `ChampSim` directory, path configurable within the script), executes the compiled `champsim_dev_baseline` binary for each trace, and redirects output.

3.  **Collecting Results:**
    * The `run.sh` script automatically parses the simulation output log (`temp_output_*.txt`) using `grep` and `awk`.
    * It extracts key metrics (IPC, Total Cycles, MPKIs, STLB Latencies, PTW Stats, Access Counts) and appends them as a new row to a CSV file (e.g., `simulation_results_traces_atp.csv`).
    * The full simulation output log for each trace is saved in a specified log directory (e.g., `simulation_logs_traces/`).

## Key Findings (Preliminary - ATP vs. iTP)

Comparing the dynamic ATP policy against the static iTP policy (using the 128-set, 12-way STLB configuration) revealed:

* **IPC:** No significant improvement; sometimes slightly worse.
* **STLB Latencies:**
    * Average *Data* Miss Latency (`STLB_Avg_dMISS_Lat`): Often improved (faster) with ATP.
    * Average *Instruction* Miss Latency (`STLB_Avg_iMISS_Lat`): Consistently and significantly worsened (slower) with ATP.
    * Overall Average Miss Latency (`STLB_Avg_MISS_Lat`): Mixed results, sometimes slightly better, sometimes much worse, often hiding the severe instruction latency penalty.
* **PTW Performance:** Average page walk latency (`PTW_Avg_Latency`) generally improved with ATP, leading to lower total cycles spent in page walks (`PTW_Total_Latency`) for most traces, despite some negative outliers.
* **STLB Misses:** ATP resulted in significantly *more* instruction misses (`STLB_iMPKI`) but often fewer data misses (`STLB_dMPKI`) compared to pure iTP.

**Conclusion:** The adaptive switching mechanism, while successful at reducing data miss latency, excessively penalized critical instruction miss performance. The current percentage-based heuristic appears suboptimal, failing to translate average latency improvements into overall IPC gains compared to the simpler, instruction-focused iTP policy. Address translation latency might not be the primary bottleneck, or the cost of increased instruction misses outweighs the benefits for data misses in these workloads.
