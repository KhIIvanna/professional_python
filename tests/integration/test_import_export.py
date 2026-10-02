from application.exporters import CSVExporter, CSVImporter

def test_csv_export_and_import_integration(tmp_path, sample_car):
    file_path = tmp_path / "vehicles.csv"
    vehicles = [sample_car]

    CSVExporter.export_to_file(vehicles, file_path)
    assert file_path.exists()

    imported = CSVImporter.import_from_file(file_path)
    assert len(imported) == 1
    assert imported[0].make == sample_car.make
    assert imported[0].model == sample_car.model
    assert imported[0].price == sample_car.price

def test_csv_export_filtered_cars_integration(tmp_path, sample_car_list):
    """3-й інтеграційний тест: експорт відфільтрованого списку авто в CSV"""
    from application.exporters import CSVExporter
    
    bmw_cars = [car for car in sample_car_list if car.make == "BMW"]
    file_path = tmp_path / "filtered_cars.csv"
    
    CSVExporter.export_to_file(bmw_cars, file_path)
    
    assert file_path.exists()
    content = file_path.read_text(encoding="utf-8")
    assert "BMW" in content
    assert "Audi" not in content