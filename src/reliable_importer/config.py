from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict
import yaml

from src.reliable_importer.exceptions import ApplicationError


@dataclass
class AppConfig:
    input_file: Path
    output_file: Path
    log_file: Path
    skip_invalid: bool = True
    min_year: int = 1900
    max_year: int = 2026
    min_price: float = 0.0
    max_price: float = 1_000_000.0
    min_mileage: int = 0
    max_mileage: int = 1_000_000


def load_config(config_path: Path) -> AppConfig:
    """Loads YAML configuration file and returns typed AppConfig dataclass."""
    if not config_path.exists():
        raise ApplicationError(f"Configuration file not found: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = yaml.safe_load(f) or {}
    except Exception as err:
        raise ApplicationError(f"Failed to parse configuration YAML: {err}") from err

    # Зчитуємо шляхи
    input_file_str = data.get("input_file") or data.get("paths", {}).get("input_csv")
    output_file_str = data.get("output_file") or data.get("paths", {}).get("output_json")
    log_file_str = data.get("log_file") or data.get("paths", {}).get("log_file")

    if not input_file_str or not output_file_str or not log_file_str:
        raise ApplicationError("Missing required paths in configuration file")

    base_dir = config_path.parent

    # Режим обробки
    skip_invalid = data.get("skip_invalid", True)
    if "processing" in data and "skip_invalid" in data["processing"]:
        skip_invalid = data["processing"]["skip_invalid"]

    # Параметри валідації з дефолтними значеннями
    val = data.get("validation", {})
    min_year = int(val.get("min_year", 1900))
    max_year = int(val.get("max_year", 2026))
    min_price = float(val.get("min_price", 0.0))
    max_price = float(val.get("max_price", 1_000_000.0))
    min_mileage = int(val.get("min_mileage", 0))
    max_mileage = int(val.get("max_mileage", 1_000_000))

    return AppConfig(
        input_file=base_dir / input_file_str,
        output_file=base_dir / output_file_str,
        log_file=base_dir / log_file_str,
        skip_invalid=skip_invalid,
        min_year=min_year,
        max_year=max_year,
        min_price=min_price,
        max_price=max_price,
        min_mileage=min_mileage,
        max_mileage=max_mileage,
    )