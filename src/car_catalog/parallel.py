from __future__ import annotations

import math
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor


def heavy_car_evaluation(price: float) -> float:
    """Імітація важкої CPU-bound математичної операції для кожного автомобіля."""
    val = price
    for _ in range(50):
        val = math.sin(val) ** 2 + math.cos(val) ** 2 + math.sqrt(abs(val) + 1)
    return val


def evaluate_cars_parallel(cars: list[dict], workers: int = 4) -> list[float]:
    """Використання ProcessPoolExecutor для паралельних CPU-bound розрахунків."""
    prices = [car["price"] for car in cars]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(heavy_car_evaluation, prices, chunksize=500))
    return results


def process_io_tasks_concurrently(
    file_names: list[str], workers: int = 4
) -> dict[str, str]:
    """Використання ThreadPoolExecutor для паралельних I/O-bound завдань (наприклад, завантаження файлів)."""

    def fake_io_load(filename: str) -> str:
        # Імітація затримки на читання файлу / мережевий запит
        return f"Дані з файлу {filename} успішно завантажено."

    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(fake_io_load, fname): fname for fname in file_names}
        results = {fname: future.result() for future, fname in futures.items()}
    return results
