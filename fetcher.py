"""Загрузка вакансий из внешних источников."""

import logging
from datetime import datetime, timedelta, timezone
from typing import Any

import requests

import config

logger = logging.getLogger(__name__)


def fetch_hh(source: dict) -> list[dict[str, Any]]:
    """Загружает вакансии с HH.ru через публичное API."""
    try:
        resp = requests.get(source["url"], params=source["params"], timeout=10)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        logger.info("HH.ru '%s': получено %d вакансий", source["params"]["text"], len(items))
        return items
    except requests.RequestException as exc:
        logger.error("Ошибка запроса HH.ru: %s", exc)
        return []


def _parse_salary(item: dict) -> tuple[int | None, int | None, str]:
    """Извлекает min/max зарплату и валюту из объекта вакансии HH.ru."""
    sal = item.get("salary") or {}
    return sal.get("from"), sal.get("to"), sal.get("currency", "")


def _is_recent(published_at: str) -> bool:
    """Возвращает True, если вакансия опубликована не позже MAX_AGE_DAYS дней назад."""
    try:
        pub = datetime.fromisoformat(published_at)
        cutoff = datetime.now(timezone.utc) - timedelta(days=config.MAX_AGE_DAYS)
        return pub >= cutoff
    except (ValueError, TypeError):
        return True


def normalize(item: dict, source_name: str) -> dict[str, Any]:
    """Приводит сырой объект HH.ru к единому формату вакансии."""
    sal_from, sal_to, currency = _parse_salary(item)
    return {
        "external_id": str(item.get("id", "")),
        "source": source_name,
        "title": item.get("name", ""),
        "company": (item.get("employer") or {}).get("name", ""),
        "url": item.get("alternate_url", ""),
        "salary_from": sal_from,
        "salary_to": sal_to,
        "currency": currency,
        "published_at": item.get("published_at", ""),
        "snippet": (item.get("snippet") or {}).get("requirement", ""),
    }


def fetch_all() -> list[dict[str, Any]]:
    """Собирает и нормализует вакансии из всех источников."""
    jobs: list[dict] = []
    for source in config.SOURCES:
        raw = fetch_hh(source)
        for item in raw:
            if not _is_recent(item.get("published_at", "")):
                continue
            jobs.append(normalize(item, source["name"]))
    # дедупликация по external_id
    seen: set[str] = set()
    unique = []
    for job in jobs:
        if job["external_id"] not in seen:
            seen.add(job["external_id"])
            unique.append(job)
    logger.info("Итого уникальных вакансий: %d", len(unique))
    return unique
