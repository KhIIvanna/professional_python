import json
from pathlib import Path
from typing import List

from src.car_catalog.models import Car
from src.reliable_importer.exceptions import DataExportError


def export_to_json_atomic(cars: List[Car], output_path: Path) -> None:
    """Writes car list to a JSON file atomically using a temporary file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = output_path.with_suffix(".tmp")

    try:
        data = [
            {
                "make": car.make,
                "model": car.model,
                "year": car.year,
                "price": car.price,
                "mileage": car.mileage,
                "full_title": car.full_title,
            }
            for car in cars
        ]
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        temp_path.replace(output_path)
    except Exception as err:
        if temp_path.exists():
            temp_path.unlink()
        raise DataExportError(
            f"Failed to export car catalog to JSON: {err}"
        ) from err