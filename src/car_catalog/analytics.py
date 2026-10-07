from __future__ import annotations

import random
from dataclasses import dataclass

import numpy as np


@dataclass
class CarAnalyticsDTO:
    make: str
    price: float
    mileage: int


def generate_car_dataset(count: int, seed: int = 42) -> list[dict]:
    """Генерує масив даних про автомобілі для бенчмарків та профілювання."""
    random.seed(seed)
    makes = [
        "Toyota",
        "BMW",
        "Audi",
        "Ford",
        "Honda",
        "Mercedes",
        "Tesla",
        "Volkswagen",
    ]
    models = ["Model A", "Model B", "Model C", "Model D"]

    dataset = []
    for i in range(count):
        dataset.append(
            {
                "id": i + 1,
                "make": random.choice(makes),
                "model": random.choice(models),
                "year": random.randint(2000, 2026),
                "price": round(random.uniform(5000.0, 100000.0), 2),
                "mileage": random.randint(0, 250000),
                "vin": f"VIN{i:014X}",
            }
        )
    return dataset


def calculate_statistics_python(cars: list[dict]) -> dict[str, float]:
    """Baseline: обчислення базової статистики звичайними циклами Python."""
    if not cars:
        return {"avg_price": 0.0, "min_price": 0.0, "max_price": 0.0, "std_price": 0.0}

    prices = [car["price"] for car in cars]
    count = len(prices)
    avg_price = sum(prices) / count
    min_price = min(prices)
    max_price = max(prices)

    variance = sum((p - avg_price) ** 2 for p in prices) / count
    std_price = variance**0.5

    return {
        "avg_price": avg_price,
        "min_price": min_price,
        "max_price": max_price,
        "std_price": std_price,
    }


def statistics_numpy(cars: list[dict]) -> dict[str, float]:
    """Оптимізована версія з використанням NumPy (векторизація)."""
    if not cars:
        return {"avg_price": 0.0, "min_price": 0.0, "max_price": 0.0, "std_price": 0.0}

    prices = np.array([car["price"] for car in cars], dtype=np.float64)
    return {
        "avg_price": float(prices.mean()),
        "min_price": float(prices.min()),
        "max_price": float(prices.max()),
        "std_price": float(prices.std()),
    }
