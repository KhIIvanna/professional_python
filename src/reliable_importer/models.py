from dataclasses import dataclass, field
from typing import List

from src.car_catalog.models import Car  


@dataclass
class ProcessingStats:
    """Model for aggregating processing statistics during ETL pipeline execution."""

    total_records: int = 0
    valid_records: int = 0
    invalid_records: int = 0
    exported_records: int = 0
    errors: List[str] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        """Calculates success rate percentage of validated records."""
        if self.total_records == 0:
            return 0.0
        return round((self.valid_records / self.total_records) * 100, 2)