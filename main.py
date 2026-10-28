"""Точка входа: запуск агрегатора вакансий."""

import argparse
import logging

import display
import fetcher
import scorer
import storage
import telegram_notify

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def run(send_telegram: bool = True) -> None:
    """Полный цикл: fetch → score → save → show → notify."""
    logger.info("=== Запуск агрегатора вакансий ===")

    # 1. Загрузка
    raw_jobs = fetcher.fetch_all()

    # 2. Скоринг и фильтрация
    jobs = scorer.filter_and_score(raw_jobs)
    logger.info("После скоринга: %d вакансий", len(jobs))

    # 3. Сохранение (возвращает только новые)
    new_jobs = storage.save(jobs)

    # 4. Отображение в консоли
    display.show(new_jobs)

    # 5. Telegram-уведомление
    if send_telegram and new_jobs:
        sent = telegram_notify.notify(new_jobs)
        logger.info("Telegram: отправлено %d из %d новых вакансий", sent, len(new_jobs))
    elif not send_telegram:
        logger.info("Telegram-уведомления отключены (--no-telegram).")

    logger.info("=== Завершено ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Агрегатор вакансий")
    parser.add_argument(
        "--no-telegram",
        action="store_true",
        help="Не отправлять уведомления в Telegram",
    )
    args = parser.parse_args()

    run(send_telegram=not args.no_telegram)
