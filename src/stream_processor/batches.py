import itertools
from typing import Generator, List, Iterable, TypeVar

T = TypeVar("T")

def batch_stream(iterable: Iterable[T], batch_size: int) -> Generator[List[T], None, None]:
    """Split an iterable stream into chunks of batch_size."""
    iterator = iter(iterable)
    while True:
        batch = list(itertools.islice(iterator, batch_size))
        if not batch:
            break
        yield batch