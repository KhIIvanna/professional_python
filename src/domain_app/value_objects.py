from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Price:
    amount: float
    currency: str = "USD"

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError("Price amount cannot be negative.")


@dataclass(frozen=True, slots=True)
class VehicleSpecification:
    engine_capacity: float
    fuel_type: str
    transmission: str