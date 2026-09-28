from typing import Generator
from car_catalog.readers import read_cars_csv
from car_catalog.parsers import parse_car_stream
from car_catalog.filters import filter_by_min_year
from car_catalog.models import Car

def build_car_pipeline(file_path: str, min_year: int = 2020) -> Generator[Car, None, None]:
    """Construct data processing stream pipeline."""
    raw_stream = read_cars_csv(file_path)
    parsed_stream = parse_car_stream(raw_stream)
    filtered_stream = filter_by_min_year(parsed_stream, min_year)
    return filtered_stream