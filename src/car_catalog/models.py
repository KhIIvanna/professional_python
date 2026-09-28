from dataclasses import dataclass

@dataclass(slots=True)
class Car:
    brand: str
    model: str
    year: int
    price: float
    mileage: int

    def __post_init__(self) -> None:
        if self.year < 1886:
            raise ValueError("Release year cannot be earlier than 1886.")
        if self.price < 0:
            raise ValueError("Price cannot be negative.")
        if self.mileage < 0:
            raise ValueError("Mileage cannot be negative.")

    @property
    def full_title(self) -> str:
        return f"{self.brand} {self.model} ({self.year})"

class CarLimitIterator:
    """First N cars from csv"""
    def __init__(self, cars: list[Car], limit: int) -> None:
        self._cars = cars
        self._limit = limit
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> Car:
        if self._index >= len(self._cars) or self._index >= self._limit:
            raise StopIteration
        car = self._cars[self._index]
        self._index += 1
        return car