"""Вывод вакансий в консоль."""

from typing import Any


def _salary_str(job: dict[str, Any]) -> str:
    """Форматирует строку зарплаты (или 'не указана')."""
    lo, hi, cur = job.get("salary_from"), job.get("salary_to"), job.get("currency", "")
    if lo and hi:
        return f"{lo:,}–{hi:,} {cur}"
    if lo:
        return f"от {lo:,} {cur}"
    if hi:
        return f"до {hi:,} {cur}"
    return "не указана"


def show(jobs: list[dict[str, Any]]) -> None:
    """Выводит список вакансий в консоль в читаемом формате."""
    if not jobs:
        print("Новых вакансий нет.")
        return

    print(f"\n{'='*60}")
    print(f"  Найдено новых вакансий: {len(jobs)}")
    print(f"{'='*60}\n")

    for i, job in enumerate(jobs, 1):
        print(f"[{i:02d}] ⭐ {job['score']:+d}  {job['title']}")
        print(f"     🏢 {job['company']}")
        print(f"     💰 {_salary_str(job)}")
        print(f"     🔗 {job['url']}")
        print()
