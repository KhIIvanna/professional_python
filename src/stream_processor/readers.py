import csv
from collections.abc import Generator


def read_cars_csv(file_path: str) -> Generator[dict[str, str], None, None]:
    """Stream CSV file row by row as dictionaries."""
    with open(file_path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        yield from reader
