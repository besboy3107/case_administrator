# Настройка DuckDB MCP сервера

## Что такое DuckDB?

DuckDB — это бесплатная аналитическая база данных SQL с открытым исходным кодом (MIT лицензия). Она идеально подходит для:
- Аналитики данных
- Работы с CSV, Parquet, JSON файлами
- Быстрых SQL запросов
- Локального анализа данных из Supabase

## Установка

Зависимости уже добавлены в `requirements.txt`. Установите их:

```bash
pip install -r requirements.txt
```

Или отдельно:
```bash
pip install duckdb mcp
```

## Настройка MCP сервера

1. **Добавьте конфигурацию в ваш IDE (Cursor)**

   Откройте настройки MCP в Cursor и добавьте:

   ```json
   {
     "mcpServers": {
       "duckdb": {
         "command": "python",
         "args": ["mcp_servers/duckdb_server.py"],
         "cwd": "${workspaceFolder}"
       }
     }
   }
   ```

   Или скопируйте содержимое файла `mcp-config.json` в настройки MCP.

2. **Перезапустите Cursor** чтобы MCP сервер загрузился

## Использование

После настройки вы сможете использовать DuckDB через MCP:

### Доступные команды:

1. **execute_sql** - Выполнить SQL запрос
   ```
   Выполни запрос: SELECT * FROM bot_actions LIMIT 10
   ```

2. **create_table** - Создать таблицу
   ```
   Создай таблицу users с полями id и name
   ```

3. **list_tables** - Показать список таблиц
   ```
   Покажи все таблицы в базе данных
   ```

4. **export_to_csv** - Экспортировать данные в CSV
   ```
   Экспортируй результат запроса в файл data/export.csv
   ```

5. **import_from_csv** - Импортировать данные из CSV
   ```
   Импортируй данные из файла data.csv в таблицу imported_data
   ```

## Примеры использования

### Анализ данных из Supabase

1. Экспортируйте данные из Supabase в CSV
2. Импортируйте в DuckDB через MCP
3. Выполняйте аналитические запросы

### Локальный анализ логов

```sql
-- Создать таблицу для логов
CREATE TABLE logs AS SELECT * FROM read_csv_auto('logs/bot_actions.csv');

-- Анализ активности пользователей
SELECT user_id, COUNT(*) as message_count 
FROM logs 
GROUP BY user_id 
ORDER BY message_count DESC;
```

## Расположение базы данных

База данных DuckDB создается в `data/analytics.duckdb` (автоматически при первом использовании).

Файл добавлен в `.gitignore`, так что он не попадет в репозиторий.

## Преимущества DuckDB

- ✅ **Бесплатная** - MIT лицензия
- ✅ **Быстрая** - оптимизирована для аналитики
- ✅ **Легкая** - не требует сервера, работает как библиотека
- ✅ **SQL совместимая** - стандартный SQL синтаксис
- ✅ **Работает с файлами** - CSV, Parquet, JSON из коробки

## Дополнительная информация

- [Официальный сайт DuckDB](https://duckdb.org/)
- [Документация DuckDB](https://duckdb.org/docs/)
- [MCP Protocol](https://modelcontextprotocol.io/)

