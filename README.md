# EljurTelegramBot README

# 📚 EljurTelegramBot — Телеграм-бот для интеграции с Eljur.ru

**Описание:**
EljurTelegramBot — это Telegram-бот, предназначенный для интеграции с системой электронного дневника Eljur.ru. Бот предоставляет пользователям удобный доступ к информации из Eljur.ru прямо в Telegram, обеспечивая быстрый и надежный способ получения актуальных данных.

**Ссылка на бота:**
👉 [@Seishun\_bot](https://t.me/Seishun_bot)

## 🚀 Особенности

* **Доступ к сообщениям:** Просмотр списка сообщений и отправка ответов.
* **Уведомления:** Получение уведомлений о новых сообщениях.
* **Домашние задания:** Просмотр актуального домашнего задания.
* **Кэширование:** Доступ к данным даже при нестабильной работе сайта Eljur.ru.

## 🛠 Технологии

* **Язык программирования:** Python 3.10+
* **Основная библиотека:** [aiogram 3.x](https://docs.aiogram.dev/en/latest/)
* **Дополнительные библиотеки:** `requests`, `aiohttp`, `asyncio`
* **Система управления зависимостями:** Pipenv
* **Развертывание:** Procfile для Heroku

## 📦 Установка и запуск

1. **Клонировать репозиторий:**

   ```bash
   git clone https://github.com/i3sey/EljurTelegramBot.git
   cd EljurTelegramBot
   ```

2. **Установить зависимости:**

   ```bash
   pip install pipenv
   pipenv install --dev
   ```

3. **Настроить переменные окружения:**

   Создайте файл `.env` в корне проекта и добавьте следующие строки:

   ```dotenv
   BOT_TOKEN=your_telegram_bot_token
   ELJUR_USERNAME=your_eljur_username
   ELJUR_PASSWORD=your_eljur_password
   ```

4. **Запустить бота:**

   ```bash
   pipenv run python run.py
   ```

## ⚙️ Структура проекта

* `run.py` — основной скрипт для запуска бота.
* `bot/` — директория с основным кодом бота.
* `Eljur/` — директория с модулями для взаимодействия с Eljur.ru.
* `.gitignore` — файл для игнорирования ненужных файлов и директорий.
* `LICENSE` — файл лицензии проекта.
* `Pipfile` и `Pipfile.lock` — файлы для управления зависимостями.
* `Procfile` — файл для развертывания на Heroku.

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](https://github.com/i3sey/EljurTelegramBot/blob/main/LICENSE).

## 📌 Примечания

* **Архивирование репозитория:** Репозиторий был заархивирован владельцем 24 января 2024 года и теперь доступен только для чтения.
* **Поддержка:** Для получения поддержки или предложения улучшений используйте раздел [Issues](https://github.com/i3sey/EljurTelegramBot/issues).

## 💡 Пример использования

1. **Запуск бота:**

   После запуска бота отправьте команду `/start` в чат с ботом.

2. **Получение сообщений:**

   Бот отобразит список ваших сообщений.

3. **Ответ на сообщение:**

   Выберите сообщение из списка и отправьте свой ответ.

4. **Просмотр домашнего задания:**

   Используйте команду `/homework` для получения актуального домашнего задания.

## 🧪 Пример кода

```python
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor

API_TOKEN = 'YOUR_BOT_TOKEN'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я EljurTelegramBot. Чем могу помочь?", parse_mode=ParseMode.MARKDOWN)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
```
