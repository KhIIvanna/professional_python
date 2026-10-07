import asyncio

from application.config import Config
from application.models import Car, CarNotFoundError, InvalidCarDataError


def add_car(catalog: list[Car], car: Car) -> None:
    if not Config.validate_car(car.year, car.price):
        raise InvalidCarDataError("Car does not meet configuration limits.")
    catalog.append(car)


def search_by_make(catalog: list[Car], make: str) -> list[Car]:
    return [c for c in catalog if c.make.lower() == make.lower()]


def search_by_model(catalog: list[Car], model: str) -> list[Car]:
    return [c for c in catalog if c.model.lower() == model.lower()]


def filter_by_year(catalog: list[Car], year: int) -> list[Car]:
    return [c for c in catalog if c.year == year]


def find_most_expensive_car(catalog: list[Car]) -> Car:
    if not catalog:
        raise CarNotFoundError("Catalog is empty.")
    return max(catalog, key=lambda c: c.price)


def calculate_average_price(catalog: list[Car]) -> float:
    if not catalog:
        return 0.0
    return sum(c.price for c in catalog) / len(catalog)


def find_lowest_mileage_car(catalog: list[Car]) -> Car:
    if not catalog:
        raise CarNotFoundError("Catalog is empty.")
    return min(catalog, key=lambda c: c.mileage)


async def fetch_external_car_price(make: str, model: str) -> float:
    await asyncio.sleep(0.01)
    if not make or not model:
        raise ValueError("Make and model are required")
    return 25000.0
