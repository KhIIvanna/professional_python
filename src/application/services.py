import asyncio
from src.car_catalog.models import Car
from src.car_catalog.services import (
    add_car,
    search_by_make,
    filter_by_year,
    find_most_expensive_car,
    calculate_average_price,
    find_lowest_mileage_car,
)

async def fetch_external_car_price(make: str, model: str) -> float:
    await asyncio.sleep(0.01)
    if not make or not model:
        raise ValueError("Make and model are required")
    return 25000.0