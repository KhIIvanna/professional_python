from car_catalog.models import Car
from car_catalog.services import (
    add_car,
    search_by_make,
    filter_by_year,
    find_most_expensive_car,
    calculate_average_price,
    find_lowest_mileage_car,
)

def main() -> None:
    cars: list[Car] = [
        Car("Toyota", "Camry", 2019, 21000.0, 75000),
        Car("BMW", "X5", 2021, 55000.0, 30000),
        Car("Toyota", "RAV4", 2022, 32000.0, 15000),
        Car("Audi", "A6", 2018, 23000.0, 110000),
    ]

    print("--- All Cars in Catalog ---")
    for car in cars:
        print(f"{car.full_title} - ${car.price:.2f}, mileage: {car.mileage} km")

    avg_price = calculate_average_price(cars)
    print(f"\nAverage car price: ${avg_price:.2f}")

    most_expensive = find_most_expensive_car(cars)
    if most_expensive:
        print(f"Most expensive car: {most_expensive.full_title} (${most_expensive.price:.2f})")

    lowest_mileage = find_lowest_mileage_car(cars)
    if lowest_mileage:
        print(f"Lowest mileage car: {lowest_mileage.full_title} ({lowest_mileage.mileage} km)")

if __name__ == "__main__":
    main()