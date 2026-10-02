import pytest

from application.models import Car

@pytest.mark.parametrize("year", [1900, 2020, 2026])
def test_valid_car_years(year):
    car = Car(make="BMW", model="X5", year=year, price=10000.0, mileage=50000)
    assert car.year == year

# 2-га параметризована функція (перевірка некоректних значень)
@pytest.mark.parametrize("price", [-1, -500.0])
def test_invalid_car_price_raises_error(price):
    with pytest.raises(ValueError):
        Car(make="BMW", model="X5", year=2020, price=price, mileage=50000)

def test_car_creation_boundary_year():
    car = Car(make="Audi", model="A6", year=1900, price=5000.0, mileage=100)
    assert car.year == 1900