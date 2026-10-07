from __future__ import annotations

from functools import lru_cache

from src.car_catalog.models import Car


def add_car(cars: list[Car], car: Car) -> None:
    cars.append(car)
    # Автоматична інвалідація кешу при додаванні нового автомобіля
    cached_calculate_average_price.cache_clear()


def search_by_make(cars: list[Car], make: str) -> list[Car]:
    return [c for c in cars if c.make.lower() == make.lower()]


def filter_by_year(cars: list[Car], min_year: int) -> list[Car]:
    return [c for c in cars if c.year >= min_year]


def find_most_expensive_car(cars: list[Car]) -> Car | None:
    return max(cars, key=lambda c: c.price, default=None)


def calculate_average_price(cars: list[Car]) -> float:
    if not cars:
        return 0.0
    return sum(c.price for c in cars) / len(cars)


def find_lowest_mileage_car(cars: list[Car]) -> Car | None:
    return min(cars, key=lambda c: c.mileage, default=None)


# --- Кешування та інвалідація ( Cache & Invalidation ) ---


@lru_cache(maxsize=128)
def cached_calculate_average_price(car_tuples: tuple[tuple, ...]) -> float:
    """Кешоване обчислення середньої ціни.
    Використовує кортежі атрибутів (price) для сумісності з lru_cache.
    """
    if not car_tuples:
        return 0.0
    total_price = sum(item[0] for item in car_tuples)  # item[0] — це price
    return total_price / len(car_tuples)


class CarCatalogCacheManager:
    """Менеджер для зручної роботи з кешем та інвалідацією списку машин у сервісах."""

    def __init__(self, cars: list[Car]):
        self._cars = cars

    def get_cars_tuple(self) -> tuple[tuple, ...]:
        return tuple((c.price,) for c in self._cars)

    def get_cached_average_price(self) -> float:
        return cached_calculate_average_price(self.get_cars_tuple())

    def clear_cache(self) -> None:
        cached_calculate_average_price.cache_clear()
