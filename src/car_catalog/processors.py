from collections import defaultdict, Counter
from car_catalog.models import Car

def get_unique_makes(cars: list[Car]) -> set[str]:
    """Set Comprehension for unique car makes."""
    return {car.make for car in cars}

def create_car_index(cars: list[Car]) -> dict[int, Car]:
    """Dict Comprehension for indexing by ID."""
    return {i + 1: car for i, car in enumerate(cars)}

def group_cars_by_make(cars: list[Car]) -> dict[str, list[Car]]:
    """defaultdict usage from collections module."""
    grouped = defaultdict(list)
    for car in cars:
        grouped[car.make].append(car)
    return dict(grouped)

def count_cars_by_make(cars: list[Car]) -> Counter:
    """Counter usage from collections module."""
    return Counter(car.make for car in cars)