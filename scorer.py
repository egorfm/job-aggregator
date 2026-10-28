"""Скоринг вакансий по ключевым словам."""

import re

import config


def _tokens(text: str) -> str:
    """Возвращает нижний регистр строки для поиска подстрок."""
    return text.lower()


def _count_matches(text: str, keywords: list[str]) -> int:
    """Считает количество совпадений слов из списка в тексте."""
    return sum(1 for kw in keywords if kw in text)


def score(job: dict) -> int:
    """
    Вычисляет релевантность вакансии.

    +2 за каждое must-have ключевое слово.
    +1 за каждое nice-to-have ключевое слово.
    -10 за любое стоп-слово (вакансия будет отфильтрована).
    """
    haystack = _tokens(
        " ".join([
            job.get("title", ""),
            job.get("snippet", ""),
        ])
    )

    # стоп-слова → сразу отбрасываем
    if _count_matches(haystack, config.EXCLUDE_KEYWORDS) > 0:
        return -10

    must = _count_matches(haystack, config.MUST_HAVE_KEYWORDS) * 2
    nice = _count_matches(haystack, config.NICE_TO_HAVE_KEYWORDS) * 1
    return must + nice


def filter_and_score(jobs: list[dict]) -> list[dict]:
    """Добавляет поле score и отфильтровывает нерелевантные вакансии."""
    scored = []
    for job in jobs:
        job["score"] = score(job)
        if job["score"] >= config.MIN_SCORE:
            scored.append(job)
    # сортировка по убыванию релевантности
    scored.sort(key=lambda j: j["score"], reverse=True)
    return scored
