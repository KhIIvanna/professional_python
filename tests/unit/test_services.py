import pytest
from unittest.mock import Mock, AsyncMock
from src.car_catalog.models import Car
from src.car_catalog.services import (
    search_by_make,
    filter_by_year,
    find_most_expensive_car,
    calculate_average_price,
    find_lowest_mileage_car,
)
from application.services import fetch_external_car_price


def test_search_by_make(sample_car_list):
    bmws = search_by_make(sample_car_list, "bmw")
    assert len(bmws) == 2
    assert all(c.make == "BMW" for c in bmws)


def test_filter_by_year(sample_car_list):
    recent = filter_by_year(sample_car_list, 2020)
    assert len(recent) == 2


def test_find_most_expensive_car(sample_car_list):
    most_expensive = find_most_expensive_car(sample_car_list)
    assert most_expensive is not None
    assert most_expensive.model == "M3"
    assert most_expensive.price == 70000.0


def test_calculate_average_price(sample_car_list):
    avg = calculate_average_price(sample_car_list)
    assert avg == pytest.approx(48333.33, rel=1e-3)


def test_calculate_average_price_empty():
    assert calculate_average_price([]) == 0.0


def test_find_lowest_mileage_car(sample_car_list):
    lowest = find_lowest_mileage_car(sample_car_list)
    assert lowest is not None
    assert lowest.mileage == 10000


def test_mock_notification():
    mock_notifier = Mock()
    mock_notifier.send("New car added")
    mock_notifier.send.assert_called_once_with("New car added")


def test_mock_notification_side_effect():
    """Вимога методички: перевірка side_effect у Mock"""
    mock_notifier = Mock()
    mock_notifier.send.side_effect = RuntimeError("Service unavailable")

    with pytest.raises(RuntimeError, match="Service unavailable"):
        mock_notifier.send("New car added")


@pytest.mark.asyncio
async def test_async_fetch_external_car_price():
    price = await fetch_external_car_price("BMW", "X5")
    assert price == 25000.0


@pytest.mark.asyncio
async def test_async_mock_external_service():
    """Вимога методички: використання AsyncMock"""
    mock_api = AsyncMock()
    mock_api.get_price.return_value = 50000.0

    result = await mock_api.get_price("BMW", "X5")
    assert result == 50000.0
    mock_api.get_price.assert_awaited_once_with("BMW", "X5")