#!/usr/bin/env python3
"""
MCP сервер для работы с DuckDB
Позволяет выполнять SQL запросы и анализировать данные через MCP
"""
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Optional

import duckdb

try:
    from mcp.server import Server
    from mcp.server.stdio import stdio_server
    from mcp.types import Tool, TextContent
except ImportError:
    # Альтернативный импорт для разных версий MCP
    try:
        from mcp.server.models import Server
        from mcp.server.stdio import stdio_server
        from mcp.types import Tool, TextContent
    except ImportError:
        print("Ошибка: MCP пакет не установлен. Установите: pip install mcp")
        sys.exit(1)

# Инициализация сервера MCP
server = Server("duckdb-mcp")

# Путь к базе данных DuckDB (можно указать свой)
DB_PATH = Path("data/analytics.duckdb")


def get_connection() -> duckdb.DuckDBPyConnection:
    """Получить подключение к DuckDB"""
    # Создаем директорию если её нет
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    # Подключаемся к базе данных (создаст файл если его нет)
    conn = duckdb.connect(str(DB_PATH))
    return conn


@server.list_tools()
async def list_tools() -> list[Tool]:
    """Список доступных инструментов"""
    return [
        Tool(
            name="execute_sql",
            description="Выполнить SQL запрос в DuckDB и вернуть результат",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL запрос для выполнения"
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="create_table",
            description="Создать таблицу в DuckDB",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Имя таблицы"
                    },
                    "schema": {
                        "type": "string",
                        "description": "SQL схема таблицы (CREATE TABLE statement)"
                    }
                },
                "required": ["table_name", "schema"]
            }
        ),
        Tool(
            name="list_tables",
            description="Показать список всех таблиц в базе данных",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="export_to_csv",
            description="Экспортировать результат запроса в CSV файл",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL запрос для выполнения"
                    },
                    "output_file": {
                        "type": "string",
                        "description": "Путь к выходному CSV файлу"
                    }
                },
                "required": ["query", "output_file"]
            }
        ),
        Tool(
            name="import_from_csv",
            description="Импортировать данные из CSV файла в таблицу",
            inputSchema={
                "type": "object",
                "properties": {
                    "csv_file": {
                        "type": "string",
                        "description": "Путь к CSV файлу"
                    },
                    "table_name": {
                        "type": "string",
                        "description": "Имя таблицы для создания"
                    }
                },
                "required": ["csv_file", "table_name"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Обработка вызовов инструментов"""
    conn = get_connection()
    
    try:
        if name == "execute_sql":
            query = arguments["query"]
            result = conn.execute(query).fetchall()
            
            # Получаем названия колонок
            try:
                description = conn.description
                columns = [desc[0] for desc in description] if description else []
            except:
                # Если description недоступен, пытаемся получить из результата
                columns = []
                if result and len(result) > 0:
                    # Пробуем получить названия из первой строки
                    try:
                        result_obj = conn.execute(query).df()
                        columns = result_obj.columns.tolist()
                        result = result_obj.values.tolist()
                    except:
                        pass
            
            # Форматируем результат
            if columns and result:
                output = {
                    "columns": columns,
                    "rows": [dict(zip(columns, row)) for row in result],
                    "row_count": len(result)
                }
            elif result:
                # Если колонок нет, возвращаем как список списков
                output = {
                    "rows": [list(row) for row in result],
                    "row_count": len(result)
                }
            else:
                output = {"message": "Запрос выполнен успешно", "row_count": 0}
            
            return [TextContent(
                type="text",
                text=json.dumps(output, indent=2, ensure_ascii=False)
            )]
        
        elif name == "create_table":
            table_name = arguments["table_name"]
            schema = arguments["schema"]
            conn.execute(schema)
            return [TextContent(
                type="text",
                text=f"Таблица '{table_name}' успешно создана"
            )]
        
        elif name == "list_tables":
            tables = conn.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
            ).fetchall()
            table_list = [table[0] for table in tables]
            return [TextContent(
                type="text",
                text=json.dumps({"tables": table_list}, indent=2, ensure_ascii=False)
            )]
        
        elif name == "export_to_csv":
            query = arguments["query"]
            output_file = arguments["output_file"]
            conn.execute(f"COPY ({query}) TO '{output_file}' (HEADER, DELIMITER ',')")
            return [TextContent(
                type="text",
                text=f"Данные экспортированы в {output_file}"
            )]
        
        elif name == "import_from_csv":
            csv_file = arguments["csv_file"]
            table_name = arguments["table_name"]
            conn.execute(f"CREATE TABLE {table_name} AS SELECT * FROM read_csv_auto('{csv_file}')")
            return [TextContent(
                type="text",
                text=f"Данные из {csv_file} импортированы в таблицу '{table_name}'"
            )]
        
        else:
            return [TextContent(
                type="text",
                text=f"Неизвестный инструмент: {name}"
            )]
    
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Ошибка: {str(e)}"
        )]
    
    finally:
        conn.close()


async def main():
    """Главная функция запуска MCP сервера"""
    from mcp.server.stdio import stdio_server
    
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

