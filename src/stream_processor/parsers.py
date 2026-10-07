from collections.abc import Generator

from src.stream_processor.models import Car


def parse_car_stream(
    raw_stream: Generator[dict[str, str], None, None],
) -> Generator[Car, None, None]:
    """Validate and convert raw dict stream into Car objects."""
    for row in raw_stream:
        try:
            yield Car(
                make=row["make"].strip(),
                model=row["model"].strip(),
                year=int(row["year"]),
                price=float(row["price"]),
                mileage=int(row["mileage"]),
            )
        except (KeyError, ValueError):
            continue
