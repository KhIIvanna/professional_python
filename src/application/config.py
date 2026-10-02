import os
from dataclasses import dataclass

@dataclass
class AppConfig:
    max_capacity: int
    environment: str

def get_config() -> AppConfig:
    max_cap = int(os.getenv("MAX_CAPACITY", "1000"))
    env = os.getenv("APP_ENV", "development")
    return AppConfig(max_capacity=max_cap, environment=env)