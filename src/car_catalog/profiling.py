from __future__ import annotations
import cProfile
import pstats
import io
import tracemalloc
from src.car_catalog.models import Car
from src.car_catalog.analytics import generate_car_dataset
from src.car_catalog.services import (
    calculate_average_price,
    search_by_make,
    filter_by_year,
    find_most_expensive_car
)

def run_heavy_workload() -> None:
    """Виконує важкі операції над великим масивом даних для профілювання."""
    print("Генерація тестового масиву даних (200 000 автомобілів)...")
    raw_data = generate_car_dataset(200_000)
    
    # Створюємо об'єкти Car відповідно до твого актуального класу з models.py
    cars = [
        Car(
            make=item["make"],
            model=item["model"],
            year=item["year"],
            price=item["price"],
            mileage=item["mileage"],
            vin=item["vin"],
            manufacturer_id=1  # умовний зв'язок з виробником
        ) for item in raw_data
    ]

    print("Запуск важких операцій (пошук, фільтрація, агрегація)...")
    _ = calculate_average_price(cars)
    _ = search_by_make(cars, "Toyota")
    _ = filter_by_year(cars, 2020)
    _ = find_most_expensive_car(cars)

def profile_with_cprofile() -> None:
    """Профілювання за допомогою cProfile."""
    pr = cProfile.Profile()
    pr.enable()
    
    run_heavy_workload()
    
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(pstats.SortKey.CUMULATIVE)
    ps.print_stats(15)  # топ 15 найповільніших функцій
    print("\n=== Результати cProfile ===")
    print(s.getvalue())

def profile_with_tracemalloc() -> None:
    """Аналіз споживання пам'яті за допомогою tracemalloc."""
    tracemalloc.start()
    
    run_heavy_workload()
    
    current, peak = tracemalloc.get_traced_memory()
    print("\n=== Результати tracemalloc ===")
    print(f"Поточне споживання пам'яті: {current / 1024 / 1024:.2f} MB")
    print(f"Пікове споживання пам'яті: {peak / 1024 / 1024:.2f} MB")
    
    tracemalloc.stop()

if __name__ == "__main__":
    print("=== Старт профілювання проєкту 'Каталог автомобілів' ===")
    profile_with_cprofile()
    profile_with_tracemalloc()