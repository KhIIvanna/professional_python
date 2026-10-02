import csv
from pathlib import Path
from typing import List
from src.car_catalog.models import Car

class CSVExporter:
    @staticmethod
    def export_to_file(cars: List[Car], file_path: Path) -> None:
        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["make", "model", "year", "price", "mileage"])
            for c in cars:
                writer.writerow([c.make, c.model, c.year, c.price, c.mileage])

class CSVImporter:
    @staticmethod
    def import_from_file(file_path: Path) -> List[Car]:
        cars: List[Car] = []
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                car = Car(
                    make=row["make"],
                    model=row["model"],
                    year=int(row["year"]),
                    price=float(row["price"]),
                    mileage=int(row["mileage"]),
                )
                cars.append(car)
        return cars