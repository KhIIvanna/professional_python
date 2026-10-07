from dataclasses import dataclass
from typing import TypedDict


class CarDict(TypedDict):
    id: int
    brand: str
    model: str
    year: int
    price: float
    mileage: int


@dataclass(slots=True)
class CreateCarDTO:
    brand: str
    model: str
    year: int
    price_amount: float
    mileage: int
    engine_capacity: float
    fuel_type: str
    transmission: str
