import csv
from pathlib import Path
from typing import Any, Dict, Generator, Tuple

from src.reliable_importer.exceptions import DataImportError


def stream_csv_rows(
    file_path: Path,
) -> Generator[Tuple[int, Dict[str, Any]], None, None]:
    """Yields (row_index, row_dict) lazily from input CSV file."""
    if not file_path.exists():
        raise DataImportError(f"Input CSV file not found: {file_path}")

    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row_idx, row in enumerate(reader, start=2):
                yield row_idx, row
    except Exception as err:
        raise DataImportError(
            f"Error occurred while streaming CSV: {err}"
        ) from err