from car_catalog.models import Car

def add_car(cars: list[Car], car: Car) -> None:
    cars.append(car)

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