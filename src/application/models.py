from dataclasses import dataclass


class InvalidCarDataError(Exception):
    """Кастомне виключення для некоректних даних автомобіля."""


class CarNotFoundError(Exception):
    """Кастомне виключення, коли авто не знайдено."""


@dataclass
class Car:
    make: str
    model: str
    year: int
    price: float
    mileage: int

    def __post_init__(self):
        if not self.make or not self.model:
            raise InvalidCarDataError("Make and model cannot be empty.")
        if self.year < 1886 or self.year > 2026:
            raise InvalidCarDataError(f"Invalid year: {self.year}")
        if self.price < 0:
            raise InvalidCarDataError(f"Invalid price: {self.price}")
        if self.mileage < 0:
            raise InvalidCarDataError(f"Invalid mileage: {self.mileage}")
