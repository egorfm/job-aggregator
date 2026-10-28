"""Отправка вакансий в Telegram через Bot API."""

import argparse
import logging
import sys
from typing import Any

import requests

import config
import storage

logger = logging.getLogger(__name__)

_API = "https://api.telegram.org/bot{token}/{method}"


def _post(method: str, payload: dict) -> bool:
    """Выполняет POST-запрос к Telegram Bot API."""
    url = _API.format(token=config.TELEGRAM_BOT_TOKEN, method=method)
    try:
        resp = requests.post(url, json=payload, timeout=10)
        resp.raise_for_status()
        return resp.json().get("ok", False)
    except requests.RequestException as exc:
        logger.error("Telegram API ошибка: %s", exc)
        return False


def _format_job(job: dict[str, Any]) -> str:
    """Формирует Markdown-сообщение для одной вакансии."""
    sal_from = job.get("salary_from")
    sal_to = job.get("salary_to")
    cur = job.get("currency", "")

    if sal_from and sal_to:
        salary = f"{sal_from:,}–{sal_to:,} {cur}"
    elif sal_from:
        salary = f"от {sal_from:,} {cur}"
    elif sal_to:
        salary = f"до {sal_to:,} {cur}"
    else:
        salary = "не указана"

    return (
        f"⭐ *{job['score']:+d}*  [{job['title']}]({job['url']})\n"
        f"🏢 {job['company']}\n"
        f"💰 {salary}"
    )


def _send_batch(jobs: list[dict[str, Any]]) -> list[str]:
    """Отправляет пачку вакансий одним сообщением. Возвращает external_id успешно отправленных."""
    lines = [_format_job(j) for j in jobs]
    header = f"🔍 *Новые вакансии* ({len(jobs)} шт.)\n\n"
    text = header + "\n\n".join(lines)

    ok = _post("sendMessage", {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    })
    if ok:
        return [j["external_id"] for j in jobs]
    return []


def notify(jobs: list[dict[str, Any]]) -> int:
    """
    Отправляет вакансии в Telegram батчами по MAX_NOTIFY штук.

    Возвращает количество успешно отправленных.
    """
    if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        logger.warning("TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не заданы — пропускаем отправку.")
        return 0

    sent_ids: list[str] = []
    batch_size = config.MAX_NOTIFY

    for start in range(0, len(jobs), batch_size):
        batch = jobs[start : start + batch_size]
        sent_ids.extend(_send_batch(batch))

    storage.mark_notified(sent_ids)
    logger.info("Отправлено в Telegram: %d вакансий", len(sent_ids))
    return len(sent_ids)


def send_test_message() -> None:
    """Отправляет тестовое сообщение для проверки подключения."""
    ok = _post("sendMessage", {
        "chat_id": config.TELEGRAM_CHAT_ID,
        "text": "✅ Job Aggregator подключён и работает!",
    })
    if ok:
        print("✅ Тестовое сообщение отправлено успешно.")
    else:
        print("❌ Не удалось отправить сообщение. Проверьте токен и chat_id.")
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    parser = argparse.ArgumentParser(description="Telegram-уведомления для Job Aggregator")
    parser.add_argument("--test", action="store_true", help="Отправить тестовое сообщение")
    parser.add_argument("--pending", action="store_true", help="Отправить все неотправленные из БД")
    args = parser.parse_args()

    if args.test:
        send_test_message()
    elif args.pending:
        pending = storage.load_unnotified()
        count = notify(pending)
        print(f"Отправлено: {count} вакансий")
    else:
        parser.print_help()
