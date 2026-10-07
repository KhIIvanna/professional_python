from collections.abc import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from application.models import Car
from application.repositories import InMemoryRepository
from src.car_catalog.database import Base
from src.car_catalog.repositories import CarDB, ManufacturerDB  # noqa: F401


@pytest.fixture
def sample_cars():
    return [
        Car(make="Toyota", model="Camry", year=2020, price=25000.0, mileage=45000),
        Car(make="BMW", model="M3", year=2022, price=75000.0, mileage=12000),
        Car(make="Toyota", model="Corolla", year=2018, price=15000.0, mileage=80000),
        Car(make="Audi", model="A4", year=2020, price=28000.0, mileage=35000),
    ]


@pytest.fixture
def empty_catalog():
    return []


@pytest.fixture
def car_repository(sample_cars):
    repo = InMemoryRepository[Car]()
    for idx, car in enumerate(sample_cars):
        repo.add(f"car_{idx}", car)
    return repo


@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """Fixture for integration tests using SQLite in-memory database."""
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
