from application.exporters import CSVExporter, CSVImporter

def test_csv_export_and_import(tmp_path, sample_car_list):
    file_path = tmp_path / "cars.csv"

    CSVExporter.export_to_file(sample_car_list, file_path)
    assert file_path.exists()

    imported_cars = CSVImporter.import_from_file(file_path)
    assert len(imported_cars) == len(sample_car_list)
    assert imported_cars[0].make == sample_car_list[0].make
    assert imported_cars[0].price == sample_car_list[0].price