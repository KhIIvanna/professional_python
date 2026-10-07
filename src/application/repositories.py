from typing import Generic, TypeVar

T = TypeVar("T")


class InMemoryRepository(Generic[T]):
    def __init__(self) -> None:
        self._storage: dict[str, T] = {}

    def add(self, key: str, item: T) -> None:
        self._storage[key] = item

    def get_by_key(self, key: str) -> T | None:
        return self._storage.get(key)

    def list_all(self) -> list[T]:
        return list(self._storage.values())
