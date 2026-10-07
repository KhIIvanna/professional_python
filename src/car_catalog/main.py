import logging
import sqlite3

from src.car_catalog import services
from src.car_catalog.config import get_settings
from src.car_catalog.database import Base, SessionLocal, engine
from src.car_catalog.models import Car
from src.car_catalog.repositories import CarRepository, ManufacturerRepository

settings = get_settings()

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("car_catalog")


def run_db_api_parameterized_query(db_path: str = "cars.db") -> None:
    logger.info("--- DB-API Parameterized Query Demo ---")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    search_make = "Toyota"
    query = "SELECT id, make, model, year, price FROM cars WHERE make = ?;"
    cursor.execute(query, (search_make,))

    rows = cursor.fetchall()
    logger.info("Direct DB-API query result for make='%s':", search_make)
    for row in rows:
        logger.info(
            "ID: %s, %s %s, Year: %s, Price: $%s",
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
        )

    conn.close()


def main() -> None:
    logger.info("Starting application in environment: %s", settings.environment)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()

    try:
        m_repo = ManufacturerRepository(session)
        c_repo = CarRepository(session)

        toyota_m = m_repo.get_by_name("Toyota") or m_repo.create("Toyota")

        if not c_repo.list_all():
            c_repo.create("Toyota", "Camry", 2021, 25000.0, 30000, toyota_m.id)
            c_repo.create("Toyota", "Corolla", 2019, 17000.0, 50000, toyota_m.id)

        db_cars = c_repo.list_all()
        dataclass_cars = [
            Car(
                make=c.make,
                model=c.model,
                year=c.year,
                price=c.price,
                mileage=c.mileage,
            )
            for c in db_cars
        ]

        avg_price = services.calculate_average_price(dataclass_cars)
        most_expensive = services.find_most_expensive_car(dataclass_cars)

        logger.info("Average Price from services: $%.2f", avg_price)
        if most_expensive:
            logger.info("Most Expensive Car: %s", most_expensive.full_title)

    finally:
        session.close()

    run_db_api_parameterized_query()


if __name__ == "__main__":
    main()
