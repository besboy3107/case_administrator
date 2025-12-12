"""Главный модуль бота"""
import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from utils.env_loader import load_env
from utils.database import Database
from filters.profanity_filter import ProfanityFilter
from handlers.message_handler import register_message_handlers
from logging_config.setup import setup_logging

logger = logging.getLogger(__name__)


async def create_bot():
    """Создание и настройка бота"""
    # Загрузка переменных окружения
    env = load_env()
    
    # Настройка логирования
    setup_logging(env['LOG_LEVEL'], env['LOG_FILE'])
    
    logger.info("Запуск Telegram-бота для модерации чатов")
    
    # Проверка наличия токена
    if not env['BOT_TOKEN']:
        raise ValueError("BOT_TOKEN не установлен в переменных окружения")
    
    # Создание бота и диспетчера
    bot = Bot(token=env['BOT_TOKEN'], parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    
    # Инициализация фильтра нецензурной лексики
    profanity_filter = ProfanityFilter()
    logger.info("Фильтр нецензурной лексики инициализирован")
    
    # Инициализация базы данных
    database = Database(
        host=env['DB_HOST'],
        port=env['DB_PORT'],
        database=env['DB_NAME'],
        user=env['DB_USER'],
        password=env['DB_PASSWORD']
    )
    
    try:
        await database.connect()
        logger.info("Подключение к базе данных установлено")
    except Exception as e:
        logger.error(f"Не удалось подключиться к базе данных: {e}")
        raise
    
    # Регистрация обработчиков
    router = register_message_handlers(profanity_filter, database)
    dp.include_router(router)
    
    return bot, dp, database


async def run_bot():
    """Запуск бота"""
    bot, dp, database = await create_bot()
    
    try:
        # Удаление вебхука (если был установлен)
        await bot.delete_webhook(drop_pending_updates=True)
        
        logger.info("Бот запущен и готов к работе")
        
        # Запуск polling
        await dp.start_polling(bot)
    
    except Exception as e:
        logger.error(f"Критическая ошибка при работе бота: {e}", exc_info=True)
    
    finally:
        # Закрытие соединений
        await database.close()
        await bot.session.close()
        logger.info("Бот остановлен")


def main():
    """Точка входа"""
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}", exc_info=True)


if __name__ == '__main__':
    main()

