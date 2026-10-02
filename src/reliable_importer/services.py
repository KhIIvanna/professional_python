import logging
from typing import List, Tuple

from src.car_catalog.models import Car
from src.car_catalog.services import add_car

from src.reliable_importer.config import AppConfig
from src.reliable_importer.exceptions import DataError, RecordValidationError
from src.reliable_importer.exporters import export_to_json_atomic
from src.reliable_importer.models import ProcessingStats
from src.reliable_importer.readers import stream_csv_rows
from src.reliable_importer.validators import validate_car_raw_data


class ImportService:
    """Orchestrates streaming import, validation using Lab 1 Car class, and export."""

    def __init__(self, config: AppConfig, logger: logging.Logger) -> None:
        self.config = config
        self.logger = logger

    def process_catalog(self) -> Tuple[List[Car], ProcessingStats]:
        """Executes full catalog import, validation, and export pipeline."""
        stats = ProcessingStats()
        valid_cars: List[Car] = []

        for row_idx, raw_row in stream_csv_rows(self.config.input_file):
            stats.total_records += 1
            try:
                validated_data = validate_car_raw_data(
                    raw_row, row_idx, self.config
                )
                car = Car(**validated_data)
                add_car(valid_cars, car)
                stats.valid_records += 1

            except (RecordValidationError, ValueError) as err:
                stats.invalid_records += 1
                err_msg = f"Row {row_idx}: {err}"
                stats.errors.append(err_msg)
                self.logger.warning(err_msg)

                if not self.config.skip_invalid:
                    raise DataError(
                        f"Aborting processing in strict mode: {err}"
                    ) from err

        if valid_cars:
            export_to_json_atomic(valid_cars, self.config.output_file)
            stats.exported_records = len(valid_cars)

        return valid_cars, stats