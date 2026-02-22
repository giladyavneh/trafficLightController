import torch
from infra.logic_functions import round_robin_logic, most_cars_logic, starvation_aware_logic, max_logic
scenarios = [
    ("Low Traffic", (1, 7), 0.5),
    ("Medium Traffic", (2, 9), 0.6),
    ("High Traffic", (3, 11), 0.7),
]

logic_functions = [
    ("Round Robin", round_robin_logic),
    ("Most Cars", most_cars_logic),
    ("Starvation Aware", starvation_aware_logic),
    ("Max Logic", max_logic)
]

if torch.cuda.is_available():
    print("CUDA detected → Running GPU benchmark\n")
    from infra.benchmark_gpu import main
else:
    print("No CUDA → Running CPU benchmark\n")
    from infra.benchmark_cpu import main

if __name__ == "__main__":
    main(scenarios, logic_functions)