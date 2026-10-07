import os


class Config:
    MIN_YEAR = int(os.getenv("MIN_YEAR", "1900"))
    MAX_PRICE = float(os.getenv("MAX_PRICE", "1000000.0"))

    @classmethod
    def validate_car(cls, year: int, price: float) -> bool:
        return cls.MIN_YEAR <= year and price <= cls.MAX_PRICE


# Додаємо аліас AppConfig та функцію get_config для сумісності з __init__.py
AppConfig = Config


def get_config():
    return Config()
