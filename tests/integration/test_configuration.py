import pytest
from application.models import Car, InvalidCarDataError
from application.services import add_car

def test_monkeypatch_min_year_config(monkeypatch, empty_catalog):
    monkeypatch.setattr("application.config.Config.MIN_YEAR", 2021)
    old_car = Car(make="Ford", model="Focus", year=2015, price=10000.0, mileage=50000)
    
    with pytest.raises(InvalidCarDataError):
        add_car(empty_catalog, old_car)