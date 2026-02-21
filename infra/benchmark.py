import torch

if torch.cuda.is_available():
    print("CUDA detected → Running GPU benchmark\n")
    from infra.benchmark_gpu import main
else:
    print("No CUDA → Running CPU benchmark\n")
    from infra.benchmark_cpu import main

if __name__ == "__main__":
    main()