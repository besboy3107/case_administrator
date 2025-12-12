# Настройка MCP (Model Context Protocol)

Проект поддерживает интеграцию с MCP серверами для расширенной работы с AI-инструментами.

## Что такое MCP?

Model Context Protocol (MCP) - это открытый протокол для интеграции AI-моделей с внешними инструментами и данными. MCP позволяет AI-ассистентам получать доступ к базам данных, API и другим ресурсам.

## Доступные MCP серверы

### 1. Supabase MCP

Интеграция с Supabase для работы с базой данных через MCP.

**Установка:**

```bash
npm install -g @supabase/mcp-server-supabase
```

**Настройка в Cursor:**

Добавьте в настройки MCP (`~/.cursor/mcp.json` или через UI):

```json
{
  "mcpServers": {
    "supabase": {
      "command": "npx",
      "args": ["-y", "@supabase/mcp-server-supabase"],
      "env": {
        "SUPABASE_URL": "https://your-project-id.supabase.co",
        "SUPABASE_SERVICE_ROLE_KEY": "your-service-role-key"
      }
    }
  }
}
```

**Где найти данные:**
- `SUPABASE_URL`: Project Settings → API → Project URL
- `SUPABASE_SERVICE_ROLE_KEY`: Project Settings → API → service_role key (секретный ключ)

### 2. Docker MCP

Управление Docker контейнерами через MCP.

**Настройка в Cursor:**

```json
{
  "mcpServers": {
    "docker": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "-v", "/var/run/docker.sock:/var/run/docker.sock", "mcp/mcp-server-docker"]
    }
  }
}
```

Или используйте уже запущенный MCP сервер Docker (если он настроен в вашей системе).

## Использование MCP

После настройки MCP серверов, ваш AI-ассистент сможет:

- **Supabase MCP:**
  - Просматривать структуру базы данных
  - Выполнять SQL запросы
  - Анализировать данные из таблицы `bot_actions`
  - Создавать и изменять таблицы

- **Docker MCP:**
  - Просматривать статус контейнеров
  - Читать логи контейнеров
  - Управлять жизненным циклом контейнеров

## Примеры использования

### Просмотр данных через Supabase MCP

```
Покажи последние 10 действий бота из базы данных
```

### Управление контейнерами через Docker MCP

```
Покажи логи контейнера telegram_moderation_bot
Проверь статус всех контейнеров проекта
```

## Дополнительные ресурсы

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [Supabase MCP Server](https://github.com/supabase/mcp-server-supabase)
- [Docker MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/docker)

