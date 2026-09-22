from car_catalog.models import Car
from car_catalog.data import INITIAL_CARS, CATALOG_METADATA
from car_catalog.processors import (
    get_unique_makes,
    create_car_index,
    group_cars_by_make,
    count_cars_by_make,
)
from car_catalog.analytics import (
    calculate_average_price,
    find_most_expensive_car,
    find_lowest_mileage_car,
    sort_cars_by_price,
    calculate_average_prices_custom,
    create_car_record,
    create_year_filter,
)

from time import perf_counter

def run_benchmark() -> None:
    """Benchmark comparing List search O(n) vs Dict lookup O(1)."""
    print("\n" + "-" * 65)
    print("EXPERIMENTAL PART: BENCHMARK")
    print("-" * 65)

    sizes = [1000, 10000, 100000]
    print(f"{'Record Count':<18} | {'List Search (sec)':<20} | {'Dict Search (sec)':<20}")
    print("-" * 65)

    for n in sizes:
        test_cars = [Car("Make", f"Model_{i}", 2020, 10000.0, 50000) for i in range(n)]
        target_id = n - 1

        start = perf_counter()
        _ = next((c for c in test_cars if c.model == f"Model_{target_id}"), None)
        list_time = perf_counter() - start

        car_dict = {f"Model_{i}": c for i, c in enumerate(test_cars)}
        start = perf_counter()
        _ = car_dict.get(f"Model_{target_id}")
        dict_time = perf_counter() - start

        print(f"{n:<18} | {list_time:<20.8f} | {dict_time:<20.8f}")

def main() -> None:
    print(f"--- {CATALOG_METADATA[0]} ({CATALOG_METADATA[1]}) ---")
    cars = INITIAL_CARS.copy()

    print("\n1. All Cars:")
    for car in cars:
        print(f" - {car.full_title}: ${car.price:.2f}, {car.mileage} km")

    print("\n2. Unique Makes (set):", get_unique_makes(cars))

    avg_price = calculate_average_price(cars)
    print(f"\n3. Average Price: ${avg_price:.2f}")

    best_car = find_most_expensive_car(cars)
    if best_car:
        print(f"   Most expensive car: {best_car.full_title} (${best_car.price:.2f})")

    min_mileage_car = find_lowest_mileage_car(cars)
    if min_mileage_car:
        print(f"   Lowest mileage car: {min_mileage_car.full_title} ({min_mileage_car.mileage} km)")

    print("\n4. Sorted by price (descending):")
    for car in sort_cars_by_price(cars):
        print(f" - {car.full_title}: ${car.price:.2f}")

    print("\n5. Car count by make (Counter):", dict(count_cars_by_make(cars)))
    print("   Grouped cars by make (defaultdict):")
    for make, group in group_cars_by_make(cars).items():
        print(f"   * {make}: {len(group)} items")

    index = create_car_index(cars)
    print("\n6. Search by ID (Dict Index) [ID=2]:", index.get(2))

    filter_2020_plus = create_year_filter(2020)
    newer_cars = [c for c in cars if filter_2020_plus(c)]
    print(f"\n7. Cars from 2020+ (Closure & List Comprehension): {len(newer_cars)} items")

    print("\n8. Demo *args:", calculate_average_prices_custom(10000.0, 20000.0, 30000.0))
    print("   Demo **kwargs:", create_car_record(make="Tesla", model="Model 3", year=2023, price=45000.0))

    run_benchmark()

if __name__ == "__main__":
    main()