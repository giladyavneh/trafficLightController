import os
import time
import torch
from concurrent.futures import ProcessPoolExecutor
from infra.simulation_runner import run_simulation, SimulationArgs
from infra.logic_functions import (
    round_robin_logic,
    most_cars_logic,
    adaptive_timer_logic,
    starvation_aware_logic,
    proportional_share_logic,
)

torch.set_num_threads(max(1, os.cpu_count() // 2))
torch.set_num_interop_threads(1)

scenarios = [
    ("Low Traffic", (1, 7), 0.5),
    ("Medium Traffic", (2, 9), 0.6),
    ("High Traffic", (3, 11), 0.7),
]

logic_functions = [
    ("Most Cars", round_robin_logic),
]

def main():
    t1 = time.perf_counter()

    tasks = [
        SimulationArgs(s[0], s[1], s[2], l[0], l[1])
        for s in scenarios
        for l in logic_functions
    ]

    with ProcessPoolExecutor() as executor:
        results = list(executor.map(run_simulation, tasks))

    print_results(results)

    print("CPU parallel duration:", time.perf_counter() - t1)

def print_results(results):
    print("\n" + "="*50)
    print(f"{'Scenario':<20} | {'Logic':<20} | {'Ticks':<10}")
    print("-" * 55)
    for r in results:
        print(f"{r[0]:<20} | {r[1]:<20} | {r[2]:<10}")
    print("="*55)

if __name__ == "__main__":
    main()