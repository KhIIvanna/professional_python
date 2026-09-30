from .value_objects import Price, VehicleSpecification
from .models import Car, ElectricCar
from .repositories import InMemoryRepository
from .services import CatalogService


class ConsoleNotifier:
    """Реалізація NotifierProtocol для виводу сповіщень у консоль."""
    def send_notification(self, message: str) -> None:
        print(f"[NOTIFICATION] {message}")


class YearFilterStrategy:
    """Стратегія фільтрації за роком випуску."""
    def __init__(self, min_year: int) -> None:
        self.min_year = min_year

    def filter(self, items: list[Car]) -> list[Car]:
        return [car for car in items if car.year >= self.min_year]


def main() -> None:
    notifier = ConsoleNotifier()
    repo = InMemoryRepository[Car]()
    service = CatalogService(repository=repo, notifier=notifier)

    spec_gas = VehicleSpecification(engine_capacity=2.0, fuel_type="Gasoline", transmission="Automatic")
    spec_ev = VehicleSpecification(engine_capacity=0.0, fuel_type="Electric", transmission="Single-speed")

    # Створення та додавання об'єктів
    car1 = Car(1, "Toyota", "Camry", 2021, Price(25000.0), 30000, spec_gas)
    car2 = ElectricCar(2, "Tesla", "Model 3", 2023, Price(40000.0), 10000, spec_ev, battery_capacity=75.0)
    car3 = Car(3, "Toyota", "Corolla", 2019, Price(18000.0), 50000, spec_gas)

    print("Додавання автомобілів")
    service.add_car(car1)
    service.add_car(car2)
    service.add_car(car3)

    print("\nЗагальна кількість та список у репозиторії (dunder-методи)")
    print(f"Total cars in catalog: {len(repo)}")
    for car in repo:
        print(f" - {car}")

    print("\nАналітика та фільтрація даних про автомобілі")
    all_cars = repo.get_all()
    
    # Найдорожчий автомобіль
    most_expensive = max(all_cars, key=lambda c: c.price.amount)
    print(f"Most expensive car: {most_expensive.brand} {most_expensive.model} ({most_expensive.price.amount} USD)")

    # Середня ціна
    avg_price = sum(c.price.amount for c in all_cars) / len(all_cars)
    print(f"Average price: {avg_price:.2f} USD")

    # Мінімальний пробіг
    min_mileage_car = min(all_cars, key=lambda c: c.mileage)
    print(f"Car with min mileage: {min_mileage_car.brand} {min_mileage_car.model} ({min_mileage_car.mileage} km)")

    print("\nФільтрація за роком")
    recent_cars = service.search(YearFilterStrategy(min_year=2021))
    print("Cars from 2021 or newer:")
    for car in recent_cars:
        print(f" - {car}")


if __name__ == "__main__":
    main()