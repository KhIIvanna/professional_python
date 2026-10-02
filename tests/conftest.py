import pytest
from src.car_catalog.models import Car

@pytest.fixture
def sample_car() -> Car:
    return Car(make="BMW", model="X5", year=2020, price=45000.0, mileage=50000)

@pytest.fixture
def sample_car_list() -> list[Car]:
    return [
        Car(make="BMW", model="X5", year=2020, price=45000.0, mileage=50000),
        Car(make="Audi", model="A6", year=2018, price=30000.0, mileage=80000),
        Car(make="BMW", model="M3", year=2022, price=70000.0, mileage=10000),
    ]