import pytest
from sqlalchemy.orm import Session

from src.car_catalog.repositories import CarRepository, ManufacturerRepository


def test_crud_operations(db_session: Session) -> None:
    m_repo = ManufacturerRepository(db_session)
    c_repo = CarRepository(db_session)

    m = m_repo.create("BMW")
    car = c_repo.create("BMW", "M3", 2022, 70000.0, 10000, m.id)

    assert car.id is not None
    assert c_repo.get_by_id(car.id) is not None

    updated = c_repo.update_price(car.id, 68000.0)
    assert updated is not None
    assert updated.price == 68000.0

    deleted = c_repo.delete(car.id)
    assert deleted is True
    assert c_repo.get_by_id(car.id) is None


def test_transaction_rollback(db_session: Session) -> None:
    m_repo = ManufacturerRepository(db_session)
    c_repo = CarRepository(db_session)

    m = m_repo.create("Ford")
    car = c_repo.create("Ford", "Focus", 2018, 12000.0, 60000, m.id)

    with pytest.raises(ValueError):
        c_repo.bulk_price_update_with_transaction(m.id, 150.0)

    reloaded_car = c_repo.get_by_id(car.id)
    assert reloaded_car is not None
    assert reloaded_car.price == 12000.0
