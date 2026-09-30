import csv
from typing import Generator, Dict

def read_cars_csv(file_path: str) -> Generator[Dict[str, str], None, None]:
    """Stream CSV file row by row as dictionaries."""
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            yield row