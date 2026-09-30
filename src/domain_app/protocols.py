from typing import Protocol, List
from .models import Car


class SearchStrategyProtocol(Protocol):
    def filter(self, items: List[Car]) -> List[Car]:
        ...


class NotifierProtocol(Protocol):
    def send_notification(self, message: str) -> None:
        ...