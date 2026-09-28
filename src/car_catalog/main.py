import sys
import csv
import time
import tracemalloc
from pathlib import Path
from itertools import islice

sys.path.append(str(Path(__file__).resolve().parent.parent))

from car_catalog.models import CarLimitIterator
from car_catalog.pipeline import build_car_pipeline
from car_catalog.analytics import calculate_streaming_metrics, group_cars_by_brand_stream


def run_benchmark_on_file(csv_file_path: str) -> None:
    print("\nPERFORMANCE BENCHMARK ON EXISTING DATASET: EAGER VS LAZY")

    tracemalloc.start()
    t_start = time.perf_counter()
    
    lazy_pipeline = build_car_pipeline(csv_file_path, min_year=0)
    lazy_count = sum(1 for _ in lazy_pipeline)
    
    lazy_time = time.perf_counter() - t_start
    _, lazy_peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    tracemalloc.start()
    t_start = time.perf_counter()
    
    with open(csv_file_path, "r", encoding="utf-8") as f:
        eager_data = list(csv.DictReader(f))
    eager_count = len(eager_data)
    
    eager_time = time.perf_counter() - t_start
    _, eager_peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    eager_mem_kb = eager_peak_mem / 1024
    lazy_mem_kb = lazy_peak_mem / 1024
    mem_ratio = eager_peak_mem / (lazy_peak_mem if lazy_peak_mem > 0 else 1)

    header = f"{'Total Records':<15} | {'Eager Time (s)':<15} | {'Lazy Time (s)':<15} | {'Eager Mem (KB)':<15} | {'Lazy Mem (KB)':<15} | {'Gain'}"
    print(header)
    print("-" * len(header))
    print(
        f"{lazy_count:<15} | "
        f"{eager_time:<15.4f} | "
        f"{lazy_time:<15.4f} | "
        f"{eager_mem_kb:<15.1f} | "
        f"{lazy_mem_kb:<15.1f} | "
        f"{mem_ratio:.1f}x"
    )


def main() -> None:
    csv_file = "data/cars_large.csv"

    sample_brands = ["Volvo", "BMW", "Nissan"]
    brand_iter = iter(sample_brands)
    print("Demo iter()/next():", next(brand_iter), next(brand_iter), next(brand_iter))

    pipeline = build_car_pipeline(csv_file, min_year=0)
    avg_price, max_car, min_car = calculate_streaming_metrics(pipeline)
    
    print(f"\nAverage price: ${avg_price:.2f}")
    if max_car:
        print(f"Most expensive car: {max_car.full_title} (${max_car.price:.2f})")
    if min_car:
        print(f"Lowest mileage car: {min_car.full_title} ({min_car.mileage} km)")

    p_islice = build_car_pipeline(csv_file, min_year=0)
    first_3 = list(islice(p_islice, 3))
    
    print("\nFirst 3 cars (via itertools.islice):")
    for car in first_3:
        print(f" - {car.full_title} (${car.price:.2f})")

    custom_iter = CarLimitIterator(first_3, limit=2)
    print("\nCustom Iterator output (limit=2):")
    for car in custom_iter:
        print(f" [CustomIter] - {car.full_title}")

    p_batch = build_car_pipeline(csv_file, min_year=0)
    first_batch = list(islice(p_batch, 5))
    print(f"\nFirst batch size: {len(first_batch)} items")

    grouped = group_cars_by_brand_stream(first_3)
    print("\nBrand distribution in selected sample:", {k: len(v) for k, v in grouped.items()})

    run_benchmark_on_file(csv_file)

if __name__ == "__main__":
    main()