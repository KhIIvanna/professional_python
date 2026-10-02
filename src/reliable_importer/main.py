from contextlib import contextmanager
import logging
from pathlib import Path
import time
from typing import Generator

from src.car_catalog.services import (
    calculate_average_price,
    find_lowest_mileage_car,
    find_most_expensive_car,
)

from src.reliable_importer.config import load_config
from src.reliable_importer.exceptions import ApplicationError
from src.reliable_importer.services import ImportService


def setup_logging(log_file: Path) -> logging.Logger:
    """Configures application logger for file and console streaming."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("reliable_importer")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


@contextmanager
def ExecutionTimer(
    operation_name: str, logger: logging.Logger
) -> Generator[None, None, None]:
    """Measures and logs execution time of encapsulated block using Context Manager."""
    start_time = time.perf_counter()
    logger.info(f"Started operation: '{operation_name}'")
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start_time
        logger.info(
            f"Finished operation: '{operation_name}' in {elapsed:.4f} seconds"
        )


def main() -> None:
    """Main execution entry point."""
    config_path = Path(__file__).resolve().parent.parent.parent / "config.yaml"

    try:
        config = load_config(config_path)
        logger = setup_logging(config.log_file)

        logger.info("=" * 50)
        logger.info("Starting Reliable Importer Pipeline (Integration with Lab 1)")

        with ExecutionTimer("Full Catalog Import Cycle", logger):
            service = ImportService(config, logger)
            cars, stats = service.process_catalog()

        logger.info("=" * 50)
        logger.info("Processing Statistics:")
        logger.info(f"Total Rows Processed: {stats.total_records}")
        logger.info(f"Successfully Validated: {stats.valid_records}")
        logger.info(f"Invalid Records: {stats.invalid_records}")
        logger.info(f"Exported Records: {stats.exported_records}")
        logger.info(f"Success Rate: {stats.success_rate}%")

        if cars:
            logger.info("=" * 50)
            logger.info("Analytics (Invoking Lab 1 car_catalog Services):")
            avg_price = calculate_average_price(cars)
            most_expensive = find_most_expensive_car(cars)
            lowest_mileage = find_lowest_mileage_car(cars)

            logger.info(f"Average Car Price: ${avg_price:.2f}")
            if most_expensive:
                logger.info(
                    f"Most Expensive: {most_expensive.full_title} - ${most_expensive.price}"
                )
            if lowest_mileage:
                logger.info(
                    f"Lowest Mileage: {lowest_mileage.full_title} - {lowest_mileage.mileage} km"
                )
        logger.info("=" * 50)

    except ApplicationError as err:
        print(f"[CRITICAL APPLICATION ERROR]: {err}")
    except Exception as err:
        print(f"[UNEXPECTED ERROR]: {err}")


if __name__ == "__main__":
    main()