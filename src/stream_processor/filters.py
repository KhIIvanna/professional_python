from collections.abc import Generator

from src.stream_processor.models import Car


def filter_by_make(
    cars_stream: Generator[Car, None, None], make: str
) -> Generator[Car, None, None]:
    """Filter cars stream by make."""
    for car in cars_stream:
        if car.make.lower() == make.lower():
            yield car


def filter_by_min_year(
    cars_stream: Generator[Car, None, None], min_year: int
) -> Generator[Car, None, None]:
    """Filter cars stream by minimum release year."""
    for car in cars_stream:
        if car.year >= min_year:
            yield car
