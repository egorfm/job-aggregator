"""Работа с SQLite БД: сохранение и дедупликация вакансий."""

import logging
import sqlite3
from typing import Any

import config

logger = logging.getLogger(__name__)

_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS jobs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    external_id TEXT NOT NULL,
    source      TEXT NOT NULL,
    title       TEXT,
    company     TEXT,
    url         TEXT,
    salary_from INTEGER,
    salary_to   INTEGER,
    currency    TEXT,
    published_at TEXT,
    snippet     TEXT,
    score       INTEGER DEFAULT 0,
    notified    INTEGER DEFAULT 0,
    saved_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(external_id, source)
)
"""


def _connect() -> sqlite3.Connection:
    """Открывает соединение и создаёт таблицу при первом запуске."""
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(_CREATE_TABLE)
    conn.commit()
    return conn


def save(jobs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    Сохраняет вакансии в БД.

    Возвращает только новые (ранее не встречавшиеся) вакансии.
    """
    conn = _connect()
    new_jobs: list[dict] = []
    for job in jobs:
        try:
            conn.execute(
                """INSERT INTO jobs
                   (external_id, source, title, company, url,
                    salary_from, salary_to, currency, published_at, snippet, score)
                   VALUES (:external_id, :source, :title, :company, :url,
                           :salary_from, :salary_to, :currency, :published_at, :snippet, :score)""",
                job,
            )
            new_jobs.append(job)
        except sqlite3.IntegrityError:
            pass  # вакансия уже есть в БД
    conn.commit()
    conn.close()
    logger.info("Сохранено новых вакансий: %d", len(new_jobs))
    return new_jobs


def mark_notified(external_ids: list[str]) -> None:
    """Помечает вакансии как отправленные в Telegram."""
    if not external_ids:
        return
    conn = _connect()
    conn.executemany(
        "UPDATE jobs SET notified=1 WHERE external_id=?",
        [(eid,) for eid in external_ids],
    )
    conn.commit()
    conn.close()


def load_unnotified() -> list[dict[str, Any]]:
    """Загружает вакансии, которые ещё не были отправлены в Telegram."""
    conn = _connect()
    rows = conn.execute(
        "SELECT * FROM jobs WHERE notified=0 ORDER BY score DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
