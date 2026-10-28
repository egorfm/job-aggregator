# Job Aggregator 🔍

Агрегатор вакансий на Python: собирает вакансии с **HH.ru**, фильтрует по ключевым словам, оценивает релевантность и отправляет новые вакансии в **Telegram**.

---

## Возможности

- Парсинг HH.ru через публичное API (без авторизации)
- Дедупликация — одна вакансия не придёт дважды
- Скоринг по must-have и nice-to-have ключевым словам
- Хранение в SQLite (локально, без сервера)
- Отправка отфильтрованных вакансий в Telegram-бот
- Флаг `--no-telegram` для тихого запуска

---

## Установка

```bash
# 1. Клонировать репозиторий
git clone https://github.com/<your-username>/job-aggregator.git
cd job-aggregator

# 2. Создать и активировать виртуальное окружение
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Установить зависимости
pip install -r requirements.txt
```

---

## Настройка Telegram

1. Откройте [@BotFather](https://t.me/BotFather) в Telegram, выполните `/newbot` и получите **токен**.
2. Напишите своему боту `/start`, затем откройте:
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
   В ответе найдите `"chat": {"id": ...}` — это ваш **CHAT_ID**.
3. Скопируйте `.env.example` в `.env` и заполните:
   ```bash
   cp .env.example .env
   ```
   ```dotenv
   TELEGRAM_BOT_TOKEN=1234567890:AABBCC...
   TELEGRAM_CHAT_ID=987654321
   ```

> **Важно:** `.env` добавлен в `.gitignore` и **никогда не попадёт в репозиторий**.

---

## Запуск

```bash
# Полный запуск: парсинг + скоринг + Telegram
python main.py

# Запуск без отправки в Telegram (только консоль)
python main.py --no-telegram

# Отправить тестовое сообщение в Telegram
python telegram_notify.py --test

# Отправить все накопленные (ещё не отправленные) вакансии из БД
python telegram_notify.py --pending
```

---

## Конфигурация (`config.py`)

| Параметр               | По умолчанию | Описание                              |
|------------------------|:------------:|---------------------------------------|
| `SOURCES`              | HH.ru ×2     | Источники и поисковые запросы         |
| `MUST_HAVE_KEYWORDS`   | python, …    | +2 балла за совпадение                |
| `NICE_TO_HAVE_KEYWORDS`| docker, …    | +1 балл за совпадение                 |
| `EXCLUDE_KEYWORDS`     | 1c, c#, …    | Вакансия отбрасывается (score = −10)  |
| `MIN_SCORE`            | 1            | Минимальный балл для сохранения       |
| `MAX_AGE_DAYS`         | 3            | Вакансии старше — игнорируются        |
| `MAX_NOTIFY`           | 10           | Максимум вакансий в одном сообщении   |
| `DB_PATH`              | jobs.db      | Путь к файлу SQLite                   |

Чтобы сменить запрос или город, отредактируйте `SOURCES` в [`config.py`](config.py).  
Список городов HH.ru: [api.hh.ru/areas](https://api.hh.ru/areas).

---

## Структура проекта

```
job-aggregator/
├── main.py             # Точка входа, оркестрация
├── fetcher.py          # Загрузка и нормализация вакансий (fetch)
├── scorer.py           # Скоринг и фильтрация (score)
├── storage.py          # Сохранение в SQLite (save)
├── display.py          # Вывод в консоль (show)
├── telegram_notify.py  # Отправка в Telegram (notify)
├── config.py           # Все настройки в одном месте
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Лицензия

MIT
