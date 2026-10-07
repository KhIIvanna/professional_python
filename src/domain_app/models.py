from abc import ABC, abstractmethod

from .value_objects import Price, VehicleSpecification


class Vehicle(ABC):
    def __init__(
        self,
        vehicle_id: int,
        brand: str,
        model: str,
        year: int,
        price: Price,
        mileage: int,
    ) -> None:
        self.id = vehicle_id
        self.brand = brand
        self.model = model
        self.year = year
        self.price = price
        self._mileage = mileage

    @abstractmethod
    def get_info(self) -> str:
        pass


class Car(Vehicle):
    def __init__(
        self,
        vehicle_id: int,
        brand: str,
        model: str,
        year: int,
        price: Price,
        mileage: int,
        spec: VehicleSpecification,
    ) -> None:
        super().__init__(vehicle_id, brand, model, year, price, mileage)
        self.spec = spec

    @property
    def mileage(self) -> int:
        return self._mileage

    @mileage.setter
    def mileage(self, value: int) -> None:
        if value < 0:
            raise ValueError("Mileage cannot be negative.")
        self._mileage = value

    def get_info(self) -> str:
        return f"{self.brand} {self.model} ({self.year}) - {self.price.amount} {self.price.currency}"

    def __str__(self) -> str:
        return self.get_info()

    def __repr__(self) -> str:
        return f"Car(id={self.id}, brand='{self.brand}', model='{self.model}', year={self.year})"


class ElectricCar(Car):
    def __init__(
        self,
        vehicle_id: int,
        brand: str,
        model: str,
        year: int,
        price: Price,
        mileage: int,
        spec: VehicleSpecification,
        battery_capacity: float,
    ) -> None:
        super().__init__(vehicle_id, brand, model, year, price, mileage, spec)
        self.battery_capacity = battery_capacity

    def get_info(self) -> str:
        base_info = super().get_info()
        return f"[EV] {base_info}, Battery: {self.battery_capacity} kWh"
