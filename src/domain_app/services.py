from .models import Car
from .protocols import NotifierProtocol, SearchStrategyProtocol
from .repositories import InMemoryRepository


class CatalogService:
    def __init__(
        self,
        repository: InMemoryRepository[Car],
        notifier: NotifierProtocol | None = None,
    ) -> None:
        self.repository = repository
        self.notifier = notifier

    def add_car(self, car: Car) -> None:
        self.repository.add(car)
        if self.notifier:
            self.notifier.send_notification(f"Added new car: {car.get_info()}")

    def search(self, strategy: SearchStrategyProtocol) -> list[Car]:
        all_cars = self.repository.get_all()
        return strategy.filter(all_cars)
