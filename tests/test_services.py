import pytest
from car_catalog.models import Car
from car_catalog.services import (
    search_by_make,
    filter_by_year,
    find_most_expensive_car,
    calculate_average_price,
    find_lowest_mileage_car,
)

def test_car_validation():
    with pytest.raises(ValueError):
        Car("Test", "Model", 1800, 1000.0, 100)

def test_search_by_make():
    cars = [
        Car("Toyota", "Camry", 2019, 21000.0, 75000),
        Car("BMW", "X5", 2021, 55000.0, 30000),
    ]
    results = search_by_make(cars, "toyota")
    assert len(results) == 1
    assert results[0].model == "Camry"

def test_calculate_average_price():
    cars = [
        Car("Toyota", "Camry", 2019, 20000.0, 75000),
        Car("BMW", "X5", 2021, 40000.0, 30000),
    ]
    assert calculate_average_price(cars) == 30000.0