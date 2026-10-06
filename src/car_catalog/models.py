from dataclasses import dataclass
from typing import Optional

@dataclass(slots=True)
class Car:
    make: str
    model: str
    year: int
    price: float
    mileage: int
    vin: Optional[str] = None  # <--- додай сюди vin, якщо його там не було
    manufacturer_id: Optional[int] = None

    def __post_init__(self) -> None:
        if self.year < 1886:
            raise ValueError("Release year cannot be earlier than 1886.")
        if self.price < 0:
            raise ValueError("Price cannot be negative.")
        if self.mileage < 0:
            raise ValueError("Mileage cannot be negative.")

    @property
    def full_title(self) -> str:
        return f"{self.make} {self.model} ({self.year})"