import asyncio
from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from src.car_catalog.database import SessionLocal, Base, engine

from src.car_catalog.repositories import (
CarRepository,
CarDB,
ManufacturerDB,
)

from src.car_catalog.schemas import CarCreate, CarResponse, CarUpdate
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Car Catalog API",
    version="1.0.0",
)
Base.metadata.create_all(bind=engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@app.get("/cars", response_model=list[CarResponse])
async def get_cars(session: Session = Depends(get_session)):
    repo = CarRepository(session)
    return repo.list_all()

@app.get("/cars/{car_id}", response_model=CarResponse)
async def get_car(car_id: int, session: Session = Depends(get_session)):
    repo = CarRepository(session)
    car = repo.get_by_id(car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Car not found")
    return car

@app.post("/cars", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
async def create_car(data: CarCreate, session: Session = Depends(get_session)):
    repo = CarRepository(session)
    car = repo.create(
        make=data.make,
        model=data.model,
        year=data.year,
        price=data.price,
        mileage=data.mileage,
        vin=data.vin,
        manufacturer_id=data.manufacturer_id,
    )
    return car

@app.patch("/cars/{car_id}", response_model=CarResponse)
async def update_car(car_id: int, data: CarUpdate, session: Session = Depends(get_session)):
    repo = CarRepository(session)
    car = repo.get_by_id(car_id)
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(car, field, value)
    
    session.commit()
    session.refresh(car)
    return car

@app.delete("/cars/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(car_id: int, session: Session = Depends(get_session)):
    repo = CarRepository(session)
    success = repo.delete(car_id)
    if not success:
        raise HTTPException(status_code=404, detail="Car not found")
    return None

@app.get("/manufacturers/{manufacturer_id}/cars", response_model=list[CarResponse])
async def get_manufacturer_cars(manufacturer_id: int, session: Session = Depends(get_session)):
    repo = CarRepository(session)
    cars = repo.list_all()
    filtered_cars = [car for car in cars if car.manufacturer_id == manufacturer_id]
    return filtered_cars

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url="/docs")

@app.post("/cars/batch", response_model=list[CarResponse], status_code=status.HTTP_200_OK)
async def get_cars_batch(car_ids: list[int], session: Session = Depends(get_session)):
    """Асинхронний endpoint для пакетного отримання даних про автомобілі за їх ID."""
    repo = CarRepository(session)
    
    cars = []
    for car_id in car_ids:
        car = repo.get_by_id(car_id)
        if car:
            cars.append(car)
            
    return cars