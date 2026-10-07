from dataclasses import dataclass


@dataclass(slots=True)
class Car:
    make: str
    model: str
    year: int
    price: float
    mileage: int

    @property
    def full_title(self) -> str:
        return f"{self.make} {self.model} ({self.year})"


class CarLimitIterator:
    """First N cars from csv"""

    def __init__(self, cars: list[Car], limit: int) -> None:
        self._cars = cars
        self._limit = limit
        self._index = 0

    def __iter__(self) -> "CarLimitIterator":
        return self

    def __next__(self) -> Car:
        if self._index >= len(self._cars) or self._index >= self._limit:
            raise StopIteration
        car = self._cars[self._index]
        self._index += 1
        return car