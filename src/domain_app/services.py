from typing import List, Optional
from .models import Car
from .repositories import InMemoryRepository
from .protocols import SearchStrategyProtocol, NotifierProtocol


class CatalogService:
    def __init__(
        self,
        repository: InMemoryRepository[Car],
        notifier: Optional[NotifierProtocol] = None,
    ) -> None:
        self.repository = repository
        self.notifier = notifier

    def add_car(self, car: Car) -> None:
        self.repository.add(car)
        if self.notifier:
            self.notifier.send_notification(f"Added new car: {car.get_info()}")

    def search(self, strategy: SearchStrategyProtocol) -> List[Car]:
        all_cars = self.repository.get_all()
        return strategy.filter(all_cars)