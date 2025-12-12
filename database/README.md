# База данных для Telegram-бота модерации

## Структура базы данных

Проект использует PostgreSQL для хранения истории действий бота.

### Таблица `bot_actions`

Хранит все действия бота:
- Входящие сообщения
- Удаленные сообщения
- Ошибки
- События удаления бота из чата

#### Поля таблицы:

| Поле | Тип | Описание |
|------|-----|----------|
| `id` | SERIAL | Уникальный идентификатор записи |
| `user_id` | BIGINT | ID пользователя Telegram |
| `chat_id` | BIGINT | ID чата |
| `action_type` | VARCHAR(50) | Тип действия (message_received, message_deleted, error, bot_removed) |
| `message_text` | TEXT | Текст сообщения |
| `timestamp` | TIMESTAMP | Время действия (автоматически) |
| `additional_data` | JSONB | Дополнительные данные в формате JSON |

#### Типы действий (action_type):

- `message_received` - получено входящее сообщение
- `message_deleted` - сообщение удалено из-за нецензурной лексики
- `error` - произошла ошибка при обработке
- `bot_removed` - бот удален из чата

## Настройка подключения

### Вариант 1: Удаленная БД (рекомендуется)

Настройте подключение в файле `.env`:

```env
DB_HOST=your_db_host
DB_PORT=5432
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
```

В `docker-compose.yml` закомментируйте блок `db` и `depends_on`.

### Вариант 2: Локальная БД в Docker

Используйте локальную БД для разработки. В `docker-compose.yml` оставьте блок `db` активным.

## Автоматическое создание таблиц

Таблицы создаются автоматически при первом запуске бота через метод `create_tables()` в `utils/database.py`.

## Примеры запросов

### Получить все удаленные сообщения за последний час:

```sql
SELECT * FROM bot_actions 
WHERE action_type = 'message_deleted' 
AND timestamp > NOW() - INTERVAL '1 hour'
ORDER BY timestamp DESC;
```

### Статистика по пользователю:

```sql
SELECT 
    user_id,
    COUNT(*) as total_actions,
    COUNT(CASE WHEN action_type = 'message_deleted' THEN 1 END) as deleted_messages
FROM bot_actions
WHERE user_id = 123456789
GROUP BY user_id;
```

### Статистика по чату:

```sql
SELECT 
    action_type,
    COUNT(*) as count
FROM bot_actions
WHERE chat_id = -1001234567890
GROUP BY action_type;
```

