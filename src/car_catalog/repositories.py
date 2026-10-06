from typing import List, Optional
from sqlalchemy import String, Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from src.car_catalog.database import Base


class ManufacturerDB(Base):
    __tablename__ = "manufacturers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    cars: Mapped[List["CarDB"]] = relationship(
        "CarDB", back_populates="manufacturer", cascade="all, delete-orphan"
    )


class CarDB(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    make: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)
    
    vin: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    manufacturer_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("manufacturers.id"), nullable=True
    )

    manufacturer: Mapped[Optional["ManufacturerDB"]] = relationship(
        "ManufacturerDB", back_populates="cars"
    )


class ManufacturerRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, name: str) -> ManufacturerDB:
        manufacturer = ManufacturerDB(name=name)
        self.session.add(manufacturer)
        self.session.commit()
        self.session.refresh(manufacturer)
        return manufacturer

    def get_by_id(self, manufacturer_id: int) -> Optional[ManufacturerDB]:
        return (
            self.session.query(ManufacturerDB)
            .filter(ManufacturerDB.id == manufacturer_id)
            .first()
        )

    def get_by_name(self, name: str) -> Optional[ManufacturerDB]:
        return (
            self.session.query(ManufacturerDB)
            .filter(ManufacturerDB.name == name)
            .first()
        )

    def list_all(self) -> List[ManufacturerDB]:
        return self.session.query(ManufacturerDB).all()


class CarRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(
        self,
        make: str,
        model: str,
        year: int,
        price: float,
        mileage: int,
        manufacturer_id: Optional[int] = None,
        vin: Optional[str] = None,
    ) -> CarDB:
        car = CarDB(
            make=make,
            model=model,
            year=year,
            price=price,
            mileage=mileage,
            manufacturer_id=manufacturer_id,
            vin=vin,
        )
        self.session.add(car)
        self.session.commit()
        self.session.refresh(car)
        return car

    def get_by_id(self, car_id: int) -> Optional[CarDB]:
        return self.session.query(CarDB).filter(CarDB.id == car_id).first()

    def list_all(self) -> List[CarDB]:
        return self.session.query(CarDB).all()

    def filter_by_make(self, make: str) -> List[CarDB]:
        return self.session.query(CarDB).filter(CarDB.make.ilike(make)).all()

    def filter_by_year(self, min_year: int) -> List[CarDB]:
        return self.session.query(CarDB).filter(CarDB.year >= min_year).all()

    def update_price(self, car_id: int, new_price: float) -> Optional[CarDB]:
        car = self.get_by_id(car_id)
        if car:
            car.price = new_price
            self.session.commit()
            self.session.refresh(car)
        return car

    def delete(self, car_id: int) -> bool:
        car = self.get_by_id(car_id)
        if car:
            self.session.delete(car)
            self.session.commit()
            return True
        return False

    def bulk_price_update_with_transaction(
        self, manufacturer_id: int, discount_percent: float
    ) -> List[CarDB]:
        """Demonstrates transaction with commit and rollback."""
        try:
            cars = (
                self.session.query(CarDB)
                .filter(CarDB.manufacturer_id == manufacturer_id)
                .all()
            )
            for car in cars:
                new_price = car.price * (1 - discount_percent / 100.0)
                if new_price < 0:
                    raise ValueError("Calculated price cannot be negative!")
                car.price = round(new_price, 2)

            self.session.commit()
            return cars
        except Exception as error:
            self.session.rollback()
            raise error