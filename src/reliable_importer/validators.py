from typing import Any

from src.reliable_importer.config import AppConfig
from src.reliable_importer.exceptions import RecordValidationError


def validate_car_raw_data(
    row: dict[str, Any], row_idx: int, config: AppConfig
) -> dict[str, Any]:
    """Validates raw CSV fields against business rules and configuration boundaries."""
    make = str(row.get("make", "")).strip()
    model = str(row.get("model", "")).strip()
    if not make or not model:
        raise RecordValidationError(
            "Fields 'make' and 'model' cannot be empty", row_idx
        )

    try:
        year = int(row["year"])
        if not (config.min_year <= year <= config.max_year):
            raise RecordValidationError(
                f"Release year {year} is out of allowed range [{config.min_year}, {config.max_year}]",
                row_idx,
            )
    except (ValueError, KeyError) as err:
        raise RecordValidationError(
            f"Invalid year value: {row.get('year')}", row_idx
        ) from err

    try:
        price = float(row["price"])
        if price < config.min_price or price > config.max_price:
            raise RecordValidationError(
                f"Price {price} is out of allowed range [{config.min_price}, {config.max_price}]",
                row_idx,
            )
    except (ValueError, KeyError) as err:
        raise RecordValidationError(
            f"Invalid price value: {row.get('price')}", row_idx
        ) from err

    try:
        mileage = int(row["mileage"])
        if mileage < 0:
            raise RecordValidationError(
                f"Mileage cannot be negative, got: {mileage}", row_idx
            )
    except (ValueError, KeyError) as err:
        raise RecordValidationError(
            f"Invalid mileage value: {row.get('mileage')}", row_idx
        ) from err

    return {
        "make": make,
        "model": model,
        "year": year,
        "price": price,
        "mileage": mileage,
    }
