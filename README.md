# Telegram-бот для модерации чатов

Полноценный Telegram-бот для автоматической модерации чатов с фильтрацией нецензурной лексики.

## Возможности

- ✅ Автоматическое удаление сообщений с нецензурной лексикой
- ✅ Подключение к удаленной PostgreSQL базе данных (Supabase)
- ✅ Логирование всех действий в файл и базу данных
- ✅ Docker-контейнеризация для простого развертывания
- ✅ Модульная архитектура
- ✅ Поддержка MCP (Model Context Protocol) для интеграции с AI-инструментами

## Структура проекта

```
.
├── bot/                    # Основной модуль бота
│   ├── __init__.py
│   └── main.py            # Главный файл запуска бота
├── handlers/              # Обработчики сообщений
│   ├── __init__.py
│   └── message_handler.py # Обработка входящих сообщений
├── filters/               # Фильтры
│   ├── __init__.py
│   └── profanity_filter.py # Фильтр нецензурной лексики
├── logging_config/        # Конфигурация логирования
│   ├── __init__.py
│   └── setup.py          # Настройка логирования
├── utils/                 # Утилиты
│   ├── __init__.py
│   ├── database.py       # Работа с БД
│   └── env_loader.py     # Загрузка переменных окружения
├── logs/                  # Директория для логов (создается автоматически)
├── main.py               # Точка входа
├── requirements.txt      # Зависимости Python
├── Dockerfile           # Образ для контейнеризации бота
├── docker-compose.yml   # Конфигурация Docker Compose
└── .env_example         # Пример файла с переменными окружения
```

## Установка и запуск

### 1. Клонирование репозитория

```bash
git clone <your-repo-url>
cd case_administrator
```

### 2. Настройка переменных окружения

Скопируйте `.env_example` в `.env` и заполните необходимые значения:

```bash
cp .env_example .env
```

Отредактируйте `.env`:

```env
# Токен Telegram бота (получите у @BotFather)
BOT_TOKEN=your_bot_token_here

# Настройки PostgreSQL для Supabase
# Получите эти данные в панели Supabase: Project Settings -> Database
DB_HOST=db.xxxxxxxxxxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=your_supabase_password

# Настройки логирования
LOG_LEVEL=INFO
LOG_FILE=logs/bot.log
```

**Подробная инструкция по настройке Supabase:** см. файл `SUPABASE_SETUP.md`

### 3. Настройка фильтра нецензурной лексики

Откройте файл `filters/profanity_filter.py` и добавьте список запрещенных слов в переменную `bad_words`:

```python
self.bad_words = [
    'слово1',
    'слово2',
    # ... добавьте свои слова
]
```

### 4. Запуск с Docker Compose

#### Вариант 1: Использование удаленной БД (рекомендуется)

1. Убедитесь, что в `docker-compose.yml` закомментирован блок `db` и `depends_on`
2. Запустите:

```bash
docker-compose up -d
```

#### Вариант 2: Использование локальной БД для разработки

1. В `docker-compose.yml` оставьте блок `db` активным
2. Запустите:

```bash
docker-compose up -d
```

### 5. Проверка работы

Проверьте логи бота:

```bash
docker-compose logs -f bot
```

Или посмотрите файл логов:

```bash
cat logs/bot.log
```

## Использование

1. Добавьте бота в ваш Telegram-чат
2. Дайте боту права администратора с возможностью удалять сообщения
3. Бот автоматически начнет модерировать чат, удаляя сообщения с нецензурной лексикой

## Логирование

Все действия бота логируются:

- **В файл**: `logs/bot.log` (с ротацией, максимум 10MB на файл, 5 резервных копий)
- **В базу данных**: таблица `bot_actions` со следующими полями:
  - `user_id` - ID пользователя
  - `chat_id` - ID чата
  - `action_type` - тип действия (message_received, message_deleted, error, bot_removed)
  - `message_text` - текст сообщения
  - `timestamp` - время действия
  - `additional_data` - дополнительные данные в формате JSON

## Структура базы данных

Таблица `bot_actions` создается автоматически при первом запуске:

```sql
CREATE TABLE bot_actions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    message_text TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    additional_data JSONB
);
```

## Остановка

```bash
docker-compose down
```

Для остановки и удаления данных БД:

```bash
docker-compose down -v
```

## Разработка

Для локальной разработки без Docker:

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск бота
python main.py
```

## Интеграция с MCP (Model Context Protocol)

Проект поддерживает интеграцию с MCP серверами для работы с AI-инструментами.

### Доступные MCP серверы:

1. **Supabase MCP** - для работы с базой данных через MCP
2. **Docker MCP** - для управления Docker контейнерами

### Настройка MCP:

MCP серверы настраиваются в вашем IDE (например, Cursor). Добавьте конфигурацию в настройки MCP:

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server-supabase"],
      "env": {
        "SUPABASE_URL": "https://your-project.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "your-service-role-key"
      }
    },
    "docker": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/mcp-server-docker"]
    }
  }
}
```

Подробнее о MCP: [Model Context Protocol Documentation](https://modelcontextprotocol.io/)

## Требования

- Python 3.11+
- PostgreSQL 12+ или Supabase
- Docker и Docker Compose (для контейнеризации)
- Node.js (для MCP серверов, опционально)

## Полезные скрипты

В проекте есть вспомогательные скрипты для работы с Docker:

- `watch-logs.bat` / `watch-logs-last.bat` - просмотр логов бота
- `open-docker.bat` / `open-docker.ps1` - открытие Docker Desktop
- `view-logs.ps1` / `view-logs.bat` - просмотр логов через PowerShell/CMD

## Лицензия

MIT

