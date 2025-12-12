"""Модуль для загрузки переменных окружения"""
import os
from dotenv import load_dotenv


def load_env():
    """Загружает переменные окружения из .env файла"""
    load_dotenv()
    
    return {
        'BOT_TOKEN': os.getenv('BOT_TOKEN'),
        'DB_HOST': os.getenv('DB_HOST'),
        'DB_PORT': int(os.getenv('DB_PORT', 5432)),
        'DB_NAME': os.getenv('DB_NAME'),
        'DB_USER': os.getenv('DB_USER'),
        'DB_PASSWORD': os.getenv('DB_PASSWORD'),
        'LOG_LEVEL': os.getenv('LOG_LEVEL', 'INFO'),
        'LOG_FILE': os.getenv('LOG_FILE', 'logs/bot.log'),
    }

