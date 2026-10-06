from __future__ import annotations
import pytest
from src.car_catalog.parallel import evaluate_cars_parallel, heavy_car_evaluation
from src.car_catalog.analytics import generate_car_dataset, calculate_statistics_python, statistics_numpy

def test_heavy_car_evaluation():
    """Перевірка окремої математичної CPU-bound операції."""
    res = heavy_car_evaluation(25000.0)
    assert isinstance(res, float)
    assert res > 0

def test_evaluate_cars_parallel_empty():
    """Перевірка паралельної обробки для порожнього списку."""
    result = evaluate_cars_parallel([], workers=2)
    assert result == []

def test_evaluate_cars_parallel_basic():
    """Перевірка паралельних обчислень на наборі словників з цінами."""
    cars_data = [
        {"price": 25000.0},
        {"price": 18000.0},
        {"price": 30000.0}
    ]
    
    results = evaluate_cars_parallel(cars_data, workers=2)
    
    assert isinstance(results, list)
    assert len(results) == len(cars_data)
    assert all(isinstance(r, float) for r in results)

def test_statistics_correctness():
    
    data = generate_car_dataset(1000)
    
    python_res = calculate_statistics_python(data)
    numpy_res = statistics_numpy(data)
    
    assert numpy_res["avg_price"] == pytest.approx(python_res["avg_price"], rel=1e-5)
    assert numpy_res["min_price"] == pytest.approx(python_res["min_price"], rel=1e-5)
    assert numpy_res["max_price"] == pytest.approx(python_res["max_price"], rel=1e-5)
    assert numpy_res["std_price"] == pytest.approx(python_res["std_price"], rel=1e-5)