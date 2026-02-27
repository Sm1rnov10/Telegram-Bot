import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    raise ValueError("Токен бота не найден! Проверьте файл .env")

PASSWORD_STRENGTH = {
    'weak': {'name': '❌ Слабый', 'color': '🔴', 'time': 'мгновенно'},
    'medium': {'name': '⚠️ Средний', 'color': '🟡', 'time': 'несколько дней'},
    'strong': {'name': '✅ Надёжный', 'color': '🟢', 'time': 'годы'},
    'very_strong': {'name': '💪 Очень надёжный', 'color': '🟣', 'time': 'столетия'}
}

DEFAULT_SETTINGS = {
    'length': 12,
    'use_lower': True,
    'use_upper': True,
    'use_digits': True,
    'use_symbols': True
}

MIN_PASSWORD_LENGTH = 4
MAX_PASSWORD_LENGTH = 64