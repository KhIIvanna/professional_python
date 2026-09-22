from car_catalog.models import Car

CATALOG_METADATA: tuple[str, str, int] = ("Car Catalog System", "v2.0", 2026)

INITIAL_CARS: list[Car] = [
    Car("Toyota", "Camry", 2019, 21000.0, 75000),
    Car("BMW", "X5", 2021, 55000.0, 30000),
    Car("Toyota", "RAV4", 2022, 32000.0, 15000),
    Car("Audi", "A6", 2018, 23000.0, 110000),
    Car("Mercedes", "C-Class", 2020, 41000.0, 45000),
]