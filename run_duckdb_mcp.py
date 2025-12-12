#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Wrapper для запуска DuckDB MCP сервера
Решает проблему с кириллицей в путях Windows
"""
import os
import sys
from pathlib import Path

# Получаем путь к директории этого скрипта
script_dir = Path(__file__).parent.absolute()

# Добавляем путь к скрипту в sys.path
sys.path.insert(0, str(script_dir))

# Меняем рабочую директорию
os.chdir(script_dir)

# Импортируем и запускаем основной сервер
if __name__ == "__main__":
    from mcp_servers.duckdb_server import main
    import asyncio
    asyncio.run(main())

