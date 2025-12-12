"""Модуль для работы с базой данных PostgreSQL"""
import asyncpg
import json
import logging
from typing import Optional, Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)


class Database:
    """Класс для работы с базой данных"""
    
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.pool: Optional[asyncpg.Pool] = None
    
    async def connect(self):
        """Подключение к базе данных и создание пула соединений"""
        try:
            self.pool = await asyncpg.create_pool(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                min_size=1,
                max_size=10
            )
            await self.create_tables()
            logger.info("Успешное подключение к базе данных")
        except Exception as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            raise
    
    async def close(self):
        """Закрытие пула соединений"""
        if self.pool:
            await self.pool.close()
            logger.info("Соединение с базой данных закрыто")
    
    async def create_tables(self):
        """Создание необходимых таблиц в базе данных"""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS bot_actions (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            chat_id BIGINT NOT NULL,
            action_type VARCHAR(50) NOT NULL,
            message_text TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            additional_data JSONB
        );
        
        CREATE INDEX IF NOT EXISTS idx_user_id ON bot_actions(user_id);
        CREATE INDEX IF NOT EXISTS idx_chat_id ON bot_actions(chat_id);
        CREATE INDEX IF NOT EXISTS idx_timestamp ON bot_actions(timestamp);
        """
        
        async with self.pool.acquire() as connection:
            await connection.execute(create_table_query)
            logger.info("Таблицы базы данных проверены/созданы")
    
    async def log_action(
        self,
        user_id: int,
        chat_id: int,
        action_type: str,
        message_text: Optional[str] = None,
        additional_data: Optional[Dict[str, Any]] = None
    ):
        """Логирование действия бота в базу данных"""
        try:
            # Преобразуем словарь в JSON строку для JSONB поля
            additional_data_json = json.dumps(additional_data) if additional_data else None
            
            async with self.pool.acquire() as connection:
                await connection.execute(
                    """
                    INSERT INTO bot_actions (user_id, chat_id, action_type, message_text, additional_data)
                    VALUES ($1, $2, $3, $4, $5::jsonb)
                    """,
                    user_id, chat_id, action_type, message_text, additional_data_json
                )
        except Exception as e:
            logger.error(f"Ошибка при записи действия в БД: {e}")

