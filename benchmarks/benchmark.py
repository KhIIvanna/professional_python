from __future__ import annotations
from time import perf_counter
from src.car_catalog.analytics import generate_car_dataset, calculate_statistics_python, statistics_numpy

def run_benchmarks():
    for size in [10_000, 100_000, 200_000]:
        data = generate_car_dataset(size)
        
        # Замір Baseline (Python loops)
        start = perf_counter()
        _ = calculate_statistics_python(data)
        python_time = perf_counter() - start
        
        # Замір NumPy
        start = perf_counter()
        _ = statistics_numpy(data)
        numpy_time = perf_counter() - start
        
        print(f"Dataset size: {size}")
        print(f"  - Python baseline: {python_time:.6f} s")
        print(f"  - NumPy vectorization: {numpy_time:.6f} s (Speedup: {python_time/numpy_time:.2f}x)")

if __name__ == "__main__":
    run_benchmarks()