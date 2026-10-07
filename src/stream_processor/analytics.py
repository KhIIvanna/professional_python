import itertools
from collections.abc import Iterable

from src.stream_processor.models import Car

def calculate_streaming_metrics(
    cars_stream: Iterable[Car],
) -> tuple[float, Car | None, Car | None]:
    total_price = 0.0
    count = 0
    max_price_car: Car | None = None
    min_mileage_car: Car | None = None

    for car in cars_stream:
        total_price += car.price
        count += 1

        if max_price_car is None or car.price > max_price_car.price:
            max_price_car = car
        if min_mileage_car is None or car.mileage < min_mileage_car.mileage:
            min_mileage_car = car

    avg_price = total_price / count if count > 0 else 0.0
    return avg_price, max_price_car, min_mileage_car


def group_cars_by_brand_stream(cars: list[Car]) -> dict[str, list[Car]]:
    """Group cars by brand using itertools.groupby after sorting."""
    sorted_cars = sorted(cars, key=lambda c: c.make)
    grouped = {}
    for make, group in itertools.groupby(sorted_cars, key=lambda c: c.make):
        grouped[make] = list(group)
    return grouped
