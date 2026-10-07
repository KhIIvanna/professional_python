import pytest

from application.models import Car


def test_car_creation_valid():
    car = Car(make="Honda", model="Civic", year=2019, price=18000.0, mileage=30000)
    assert car.make == "Honda"
    assert car.model == "Civic"
    assert car.year == 2019
    assert car.price == pytest.approx(18000.0)
    assert car.mileage == 30000


def test_repository_add_and_get(car_repository):
    all_items = car_repository.list_all()
    assert len(all_items) == 4
    retrieved = car_repository.get_by_key("car_0")
    assert retrieved is not None
    assert retrieved.make == "Toyota"
