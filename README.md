<h1 align="center">🔍 job-aggregator</h1>

<p align="center">
  Агрегатор IT-вакансий с HeadHunter (HH.ru) с гибким скорингом релевантности и уведомлениями в Telegram
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/API-HH.ru-red?logo=hh.ru" alt="HH API">
  <img src="https://img.shields.io/badge/Telegram-Bot%20API-2CA5E0?logo=telegram&logoColor=white" alt="Telegram">
  <img src="https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite&logoColor=white" alt="SQLite">
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License">
</p>

---

## ✨ Возможности

- 🌐 **Сбор без авторизации**: парсинг вакансий через официальное публичное API HH.ru.
- 🎯 **Умный скоринг**: оценка соответствия по спискам `must-have`, `nice-to-have` и исключающим стоп-словам.
- 🚫 **Дедупликация**: встроенный трекинг уже обработанных вакансий исключает повторные уведомления.
- 📱 **Telegram-уведомления**: автоматическая отправка подходящих вакансий с прямыми ссылками и ключевыми данными.
- 🤫 **Тихий режим**: поддержка флага `--no-telegram` для отладки и вывода только в консоль.
- 💾 **Локальная база данных**: хранение вакансий в SQLite без необходимости разворачивать сервер БД.

---

## 🛠 Стек технологий

- **Python 3.10+**
- **Requests** — взаимодействие с публичным API HeadHunter
- **SQLite3** — локальное хранение вакансий
- **Python-dotenv** — управление токенами и конфигурацией

---

## 🚀 Быстрый старт

### 1. Клонирование репозитория
```bash
git clone https://github.com/egorfm/job-aggregator.git
cd job-aggregator
```

### 2. Создание и активация виртуального окружения
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Настройка Telegram-уведомлений
1. Получите токен бота у [@BotFather](https://t.me/BotFather).
2. Узнайте свой `CHAT_ID` (напишите боту `/start` и откройте `https://api.telegram.org/bot<TOKEN>/getUpdates`).
3. Скопируйте шаблон окружения и укажите свои параметры:
```bash
cp .env.example .env
```
Заполните в `.env`:
```ini
TELEGRAM_BOT_TOKEN="ваш_токен_бота"
TELEGRAM_CHAT_ID="ваш_chat_id"
```

---

## 💻 Использование

```bash
# Полный цикл: сбор + скоринг + отправка в Telegram
python main.py

# Запуск в тихом режиме (только вывод в терминал)
python main.py --no-telegram

# Проверка отправки тестового сообщения в Telegram
python telegram_notify.py --test

# Отправка неотправленных вакансий из базы данных
python telegram_notify.py --pending
```

---

## ⚙️ Конфигурация (`config.py`)

| Параметр | Описание |
|---|---|
| `SOURCES` | Список поисковых запросов и идентификаторы регионов HH.ru |
| `MUST_HAVE_KEYWORDS` | Обязательные ключевые слова (+2 балла к рейтингу) |
| `NICE_TO_HAVE_KEYWORDS` | Желательные навыки (+1 балл к рейтингу) |
| `EXCLUDE_KEYWORDS` | Стоп-слова (отсеивают вакансию) |
| `MIN_SCORE` | Минимальный порог баллов для сохранения |
| `MAX_AGE_DAYS` | Максимальный возраст вакансии для обработки (в днях) |

---

## 📁 Структура проекта

```
job-aggregator/
├── main.py             # Точка входа и оркестрация процесса
├── fetcher.py          # Сбор и нормализация данных с API HH.ru
├── scorer.py           # Скоринг и фильтрация по ключевым словам
├── storage.py          # Работа с локальной базой данных SQLite
├── display.py          # Форматированный вывод результатов в терминал
├── telegram_notify.py  # Модуль отправки уведомлений в Telegram
├── config.py           # Параметры поиска, фильтрации и весов
├── requirements.txt    # Зависимости проекта
├── .env.example        # Пример конфигурации
├── LICENSE             # Лицензия MIT
└── README.md
```

---

## 📄 Лицензия

Проект распространяется под лицензией [MIT](LICENSE).
