from src.car_catalog.models import Car

def test_car_creation_and_full_title(sample_car):
    assert sample_car.make == "BMW"
    assert sample_car.model == "X5"
    assert sample_car.full_title == "BMW X5 (2020)"