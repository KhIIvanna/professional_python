from typing import Protocol

from .models import Car


class SearchStrategyProtocol(Protocol):
    def filter(self, items: list[Car]) -> list[Car]: ...


class NotifierProtocol(Protocol):
    def send_notification(self, message: str) -> None: ...
