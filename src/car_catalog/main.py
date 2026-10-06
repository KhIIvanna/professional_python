import sqlite3
from src.car_catalog.database import engine, Base, SessionLocal
from src.car_catalog.repositories import ManufacturerRepository, CarRepository
from src.car_catalog.models import Car
from src.car_catalog import services


def run_db_api_parameterized_query(db_path: str = "cars.db") -> None:
    print("\n--- DB-API Parameterized Query Demo ---")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    search_make = "Toyota"
    query = "SELECT id, make, model, year, price FROM cars WHERE make = ?;"
    cursor.execute(query, (search_make,))
    
    rows = cursor.fetchall()
    print(f"Direct DB-API query result for make='{search_make}':")
    for row in rows:
        print(f"ID: {row[0]}, {row[1]} {row[2]}, Year: {row[3]}, Price: ${row[4]}")
    
    conn.close()


def main() -> None:
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    try:
        m_repo = ManufacturerRepository(session)
        c_repo = CarRepository(session)

        toyota_m = m_repo.get_by_name("Toyota") or m_repo.create("Toyota")

        if not c_repo.list_all():
            c_repo.create("Toyota", "Camry", 2021, 25000.0, 30000, toyota_m.id)
            c_repo.create("Toyota", "Corolla", 2019, 17000.0, 50000, toyota_m.id)

        # Using your existing memory-based services with dataclasses
        db_cars = c_repo.list_all()
        dataclass_cars = [
            Car(make=c.make, model=c.model, year=c.year, price=c.price, mileage=c.mileage)
            for c in db_cars
        ]

        avg_price = services.calculate_average_price(dataclass_cars)
        most_expensive = services.find_most_expensive_car(dataclass_cars)

        print(f"Average Price from services: ${avg_price:.2f}")
        if most_expensive:
            print(f"Most Expensive Car: {most_expensive.full_title}")

    finally:
        session.close()

    run_db_api_parameterized_query()


if __name__ == "__main__":
    main()