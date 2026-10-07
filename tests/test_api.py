from fastapi.testclient import TestClient

from src.car_catalog.api import app

client = TestClient(app)


def test_get_cars():
    response = client.get("/cars")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_and_delete_car():
    response = client.post(
        "/cars",
        json={
            "make": "Toyota",
            "model": "Camry",
            "year": 2022,
            "price": 30000.0,
            "mileage": 15000,
            "vin": "1HGCR2F83HA000001",
        },
    )
    assert response.status_code == 201
    data = response.json()
    car_id = data["id"]
    assert data["make"] == "Toyota"

    # Видалення створеного авто
    del_response = client.delete(f"/cars/{car_id}")
    assert del_response.status_code == 204


def test_invalid_car_data():
    response = client.post(
        "/cars",
        json={
            "make": "Toyota",
            "model": "Camry",
            "year": 1500,  # Некоректний рік (валідація Pydantic)
            "price": -100,  # Некоректна ціна
            "mileage": 1000,
        },
    )
    assert response.status_code == 422
