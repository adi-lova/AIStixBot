# AIStixBot

Telegram-бот для генерации стикеров с использованием Google Colab и aiogram.

## Установка

1. Клонируйте репозиторий:
git clone https://github.com/adi-lova/AIStixBot.git


2. Установите зависимости:
pip install -r requirements.txt


3. Создайте файл `.env` и добавьте токен бота и ссылку на Colab:
BOT_TOKEN=your_telegram_bot_token
COLAB_URL=https://colab.research.google.com/drive/your_colab_notebook_id


4. Запустите бота:
python main.py


## Функциональность

- Генерация стикеров по описанию
- Выбор стиля (аниме, реализм, чиби)
- Выбор фона (с фоном, без фона)
- Выбор количества стикеров
- Создание стикеров из фотографий