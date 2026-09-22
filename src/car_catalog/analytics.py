from typing import Callable
from car_catalog.models import Car
from car_catalog.decorators import measure_time

@measure_time
def calculate_average_price(cars: list[Car]) -> float:
    """Calculate average price using a generator expression."""
    if not cars:
        return 0.0
    return sum(car.price for car in cars) / len(cars)

def find_most_expensive_car(cars: list[Car]) -> Car | None:
    """Lambda usage for finding the most expensive car."""
    return max(cars, key=lambda c: c.price, default=None)

def find_lowest_mileage_car(cars: list[Car]) -> Car | None:
    """Lambda usage for finding the car with the lowest mileage."""
    return min(cars, key=lambda c: c.mileage, default=None)

def sort_cars_by_price(cars: list[Car], reverse: bool = True) -> list[Car]:
    """Sort cars by price."""
    return sorted(cars, key=lambda c: c.price, reverse=reverse)

def calculate_average_prices_custom(*prices: float) -> float:
    """Calculate average price using positional arguments (*args)."""
    if not prices:
        return 0.0
    return sum(prices) / len(prices)

def create_car_record(**kwargs) -> dict:
    """Create a car dictionary using keyword arguments (**kwargs)."""
    return dict(kwargs)

def create_year_filter(min_year: int) -> Callable[[Car], bool]:
    """Closure factory for filtering cars by minimum year."""
    def predicate(car: Car) -> bool:
        return car.year >= min_year
    return predicate