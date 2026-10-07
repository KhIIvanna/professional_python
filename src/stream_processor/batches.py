import itertools
from collections.abc import Generator, Iterable
from typing import TypeVar

T = TypeVar("T")


def batch_stream(
    iterable: Iterable[T], batch_size: int
) -> Generator[list[T], None, None]:
    """Split an iterable stream into chunks of batch_size."""
    iterator = iter(iterable)
    while True:
        batch = list(itertools.islice(iterator, batch_size))
        if not batch:
            break
        yield batch
