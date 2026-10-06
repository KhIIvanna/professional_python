import pytest
from unittest.mock import AsyncMock
from application.models import CarNotFoundError
from application.services import (
    search_by_make,
    search_by_model,
    filter_by_year,
    find_most_expensive_car,
    calculate_average_price,
    find_lowest_mileage_car,
    fetch_external_car_price,
)

def test_search_by_make(sample_cars):
    results = search_by_make(sample_cars, "Toyota")
    assert len(results) == 2

def test_search_by_model(sample_cars):
    results = search_by_model(sample_cars, "M3")
    assert len(results) == 1
    assert results[0].model == "M3"

def test_filter_by_year(sample_cars):
    results = filter_by_year(sample_cars, 2020)
    assert len(results) == 2

def test_find_most_expensive_car(sample_cars):
    car = find_most_expensive_car(sample_cars)
    assert car.model == "M3"
    assert car.price == pytest.approx(75000.0)

def test_find_most_expensive_car_empty_raises(empty_catalog):
    with pytest.raises(CarNotFoundError):
        find_most_expensive_car(empty_catalog)

def test_calculate_average_price(sample_cars):
    avg = calculate_average_price(sample_cars)
    assert avg == pytest.approx(35750.0)

def test_calculate_average_price_empty(empty_catalog):
    assert calculate_average_price(empty_catalog) == pytest.approx(0.0)

def test_find_lowest_mileage_car(sample_cars):
    car = find_lowest_mileage_car(sample_cars)
    assert car.model == "M3"
    assert car.mileage == 12000

def test_find_lowest_mileage_car_empty_raises(empty_catalog):
    with pytest.raises(CarNotFoundError):
        find_lowest_mileage_car(empty_catalog)

@pytest.mark.asyncio
async def test_fetch_external_car_price_async():
    price = await fetch_external_car_price("Tesla", "Model 3")
    assert price == pytest.approx(25000.0)

@pytest.mark.asyncio
async def test_fetch_external_car_price_mock():
    mock_service = AsyncMock(return_value=32000.0)
    price = await mock_service("BMW", "X5")
    assert price == pytest.approx(32000.0)
    mock_service.assert_called_once_with("BMW", "X5")

@pytest.mark.asyncio
async def test_fetch_external_car_price_failure():
    mock_service = AsyncMock(side_effect=ValueError("Service unavailable"))
    with pytest.raises(ValueError, match="Service unavailable"):
        await mock_service("BMW", "X5")