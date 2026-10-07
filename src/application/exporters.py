import csv
import json
from pathlib import Path

from application.models import Car, InvalidCarDataError


class CSVExporter:
    @staticmethod
    def export_to_file(cars: list[Car], file_path: Path) -> None:
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["make", "model", "year", "price", "mileage"])
            for c in cars:
                writer.writerow([c.make, c.model, c.year, c.price, c.mileage])


class CSVImporter:
    @staticmethod
    def import_from_file(file_path: Path) -> list[Car]:
        cars: list[Car] = []
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_idx, row in enumerate(reader, start=2):
                try:
                    car = Car(
                        make=row["make"],
                        model=row["model"],
                        year=int(row["year"]),
                        price=float(row["price"]),
                        mileage=int(row["mileage"]),
                    )
                    cars.append(car)
                except (KeyError, ValueError) as e:
                    raise InvalidCarDataError(
                        f"Malformed CSV record at line {row_idx}: {e}"
                    )
        return cars


class JSONExporter:
    @staticmethod
    def export_to_file(cars: list[Car], file_path: Path) -> None:
        data = [
            {
                "make": c.make,
                "model": c.model,
                "year": c.year,
                "price": c.price,
                "mileage": c.mileage,
            }
            for c in cars
        ]
        with open(file_path, mode="w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
