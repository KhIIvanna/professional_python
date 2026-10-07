# Car Catalog REST API Service

Проєкт розроблено в межах курсу **Professional Python**. Сервіс надає REST API для управління каталогом автомобілів та їх виробників, підтримує асинхронні запити, інтеграцію з бази даних через SQLAlchemy ORM, а також повний цикл контейнеризації та CI/CD.

# Основні можливості

- **REST API (FastAPI)**: CRUD-операції для автомобілів, пакетна обробка даних, фільтрація за виробником.
- **База даних (SQLAlchemy)**: Підтримка SQLite / PostgreSQL через конфігуратор ресурсів.
- **Конфігурація (Pydantic Settings)**: Управління змінними середовища через `.env` файли.
- **Healthcheck & Monitoring**: Ендпоінт `/health` для моніторингу стану сервісу.
- **Логування**: Стандартний модуль `logging` із гнучким рівнем деталізації (`LOG_LEVEL`).
- **Контейнеризація**: Повна підтримка Docker та Docker Compose.
- **CI/CD**: Готовий GitHub Actions pipeline (лінтинг, перевірка типів, тести, збірка Docker).

# Структура проєкту

car-catalog/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI/CD Pipeline
├── src/
│   └── car_catalog/
│       ├── __init__.py
│       ├── api.py             # FastAPI ендпоінти (/cars, /health тощо)
│       ├── config.py          # Pydantic Settings конфігурація
│       ├── database.py        # SQLAlchemy Engine & SessionLocal
│       ├── main.py            # CLI/Демо-скрипт із логуванням
│       ├── models.py          # SQLAlchemy ORM моделі
│       ├── repositories.py    # Патерн Repository для роботи з БД
│       ├── schemas.py         # Pydantic валидаційні схеми
│       └── services.py        # Бізнес-логіка та обчислення
├── tests/
│   ├── conftest.py            # Pytest фікстури (тестова БД, async client)
│   ├── test_api.py            # Інтеграційні тести API
│   └── test_services.py       # Юніт-тести бізнес-логіки
├── .dockerignore
├── .env.example               # Шаблон змінних середовища
├── .gitignore
├── Dockerfile                 # Docker-образ для production
├── pyproject.toml             # Налаштування пакувальника, залежностей, Ruff та Mypy
└── README.md                  # Документація проєкту