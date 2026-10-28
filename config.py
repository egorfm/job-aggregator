"""Централизованные настройки агрегатора вакансий."""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Telegram ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# --- Источники ---
SOURCES = [
    {
        "name": "HH.ru",
        "url": "https://api.hh.ru/vacancies",
        "params": {
            "text": "Python разработчик",
            "area": 1,          # 1 = Москва
            "per_page": 20,
            "order_by": "publication_time",
        },
    },
    {
        "name": "HH.ru",
        "url": "https://api.hh.ru/vacancies",
        "params": {
            "text": "Backend developer",
            "area": 1,
            "per_page": 20,
            "order_by": "publication_time",
        },
    },
]

# --- Скоринг: ключевые слова ---
MUST_HAVE_KEYWORDS = ["python", "fastapi", "django", "flask", "asyncio"]
NICE_TO_HAVE_KEYWORDS = ["postgresql", "redis", "docker", "kubernetes", "aws", "kafka"]
EXCLUDE_KEYWORDS = ["1c", "1с", "c#", "java ", ".net"]

# --- Фильтры ---
MIN_SCORE = 1           # минимальный балл для сохранения вакансии
MAX_AGE_DAYS = 3        # отсекаем старые вакансии (дней)

# --- БД ---
DB_PATH = "jobs.db"

# --- Уведомления ---
MAX_NOTIFY = 10         # максимум вакансий в одном Telegram-сообщении
