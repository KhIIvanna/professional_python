class ApplicationError(Exception):
    """Base exception class for all application errors."""


class ConfigurationError(ApplicationError):
    """Raised when configuration loading or validation fails."""


class DataError(ApplicationError):
    """Base exception class for data processing errors."""


class RecordValidationError(DataError):
    """Raised when validation fails for a specific car record."""

    def __init__(self, message: str, row_index: int | None = None) -> None:
        super().__init__(message)
        self.row_index = row_index


class DataImportError(DataError):
    """Raised when critical errors occur during CSV data import."""


class DataExportError(DataError):
    """Raised when atomic file writing or JSON serialization fails."""
