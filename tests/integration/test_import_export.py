import pytest
from application.exporters import CSVExporter, CSVImporter, JSONExporter
from application.models import InvalidCarDataError
from application.services import search_by_make, calculate_average_price

def test_csv_export_import_integration(tmp_path, sample_cars):
    file_path = tmp_path / "cars.csv"
    CSVExporter.export_to_file(sample_cars, file_path)
    assert file_path.exists()

    imported_cars = CSVImporter.import_from_file(file_path)
    assert len(imported_cars) == len(sample_cars)
    assert imported_cars[0].make == sample_cars[0].make
    assert imported_cars[0].price == pytest.approx(sample_cars[0].price)

def test_csv_import_malformed_record_raises(tmp_path):
    file_path = tmp_path / "malformed.csv"
    file_path.write_text("make,model,year,price,mileage\nToyota,Camry,INVALID_YEAR,25000,45000", encoding="utf-8")

    with pytest.raises(InvalidCarDataError):
        CSVImporter.import_from_file(file_path)

def test_json_export_integration(tmp_path, sample_cars):
    file_path = tmp_path / "cars.json"
    JSONExporter.export_to_file(sample_cars, file_path)
    assert file_path.exists()
    assert file_path.stat().st_size > 0

def test_full_data_pipeline(tmp_path, sample_cars):
    csv_file = tmp_path / "pipeline.csv"
    CSVExporter.export_to_file(sample_cars, csv_file)
    
    loaded_cars = CSVImporter.import_from_file(csv_file)
    toyotas = search_by_make(loaded_cars, "Toyota")
    avg_price = calculate_average_price(toyotas)
    
    assert len(toyotas) == 2
    assert avg_price == pytest.approx(20000.0)