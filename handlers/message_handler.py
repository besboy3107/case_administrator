"""Обработчик сообщений для модерации чата"""
import logging
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, LEFT
from aiogram.filters.chat_member_updated import ChatMemberUpdated

from filters.profanity_filter import ProfanityFilter
from utils.database import Database

logger = logging.getLogger(__name__)

router = Router()


def register_message_handlers(profanity_filter: ProfanityFilter, database: Database):
    """
    Регистрация обработчиков сообщений
    
    Args:
        profanity_filter: Экземпляр фильтра нецензурной лексики
        database: Экземпляр базы данных
    """
    
    @router.message(F.text | F.caption)
    async def handle_message(message: Message):
        """Обработка текстовых сообщений и подписей к медиа"""
        try:
            # Работаем только в группах и супергруппах
            if message.chat.type not in ['group', 'supergroup']:
                return
            
            # Получаем текст сообщения
            text = message.text or message.caption
            if not text:
                return
            
            user_id = message.from_user.id if message.from_user else None
            chat_id = message.chat.id
            username = message.from_user.username if message.from_user else "Неизвестно"
            
            # Логируем входящее сообщение
            logger.info(
                f"Входящее сообщение от пользователя {user_id} (@{username}) "
                f"в чате {chat_id}: {text[:100]}"
            )
            
            # Логируем в БД
            await database.log_action(
                user_id=user_id or 0,
                chat_id=chat_id,
                action_type='message_received',
                message_text=text,
                additional_data={
                    'username': username,
                    'message_id': message.message_id
                }
            )
            
            # Проверяем на нецензурную лексику
            if profanity_filter.contains_profanity(text):
                try:
                    # Удаляем сообщение
                    await message.delete()
                    
                    logger.warning(
                        f"Удалено сообщение от пользователя {user_id} (@{username}) "
                        f"в чате {chat_id} из-за нецензурной лексики"
                    )
                    
                    # Логируем удаление в БД
                    await database.log_action(
                        user_id=user_id or 0,
                        chat_id=chat_id,
                        action_type='message_deleted',
                        message_text=text,
                        additional_data={
                            'username': username,
                            'message_id': message.message_id,
                            'reason': 'profanity'
                        }
                    )
                    
                except Exception as e:
                    error_msg = f"Ошибка при удалении сообщения: {e}"
                    logger.error(error_msg)
                    
                    # Логируем ошибку в БД
                    await database.log_action(
                        user_id=user_id or 0,
                        chat_id=chat_id,
                        action_type='error',
                        message_text=text,
                        additional_data={
                            'username': username,
                            'message_id': message.message_id,
                            'error': str(e)
                        }
                    )
        
        except Exception as e:
            logger.error(f"Ошибка при обработке сообщения: {e}", exc_info=True)
    
    @router.my_chat_member(ChatMemberUpdatedFilter(member_status_changed=KICKED | LEFT))
    async def handle_bot_removed(event: ChatMemberUpdated):
        """Обработка события удаления бота из чата"""
        chat_id = event.chat.id
        logger.info(f"Бот удален из чата {chat_id}")
        
        await database.log_action(
            user_id=0,
            chat_id=chat_id,
            action_type='bot_removed',
            additional_data={
                'chat_title': event.chat.title
            }
        )
    
    return router

