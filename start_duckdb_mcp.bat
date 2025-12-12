@echo off
REM Обертка для запуска DuckDB MCP сервера
REM Решает проблему с кириллицей в пути

cd /d "%~dp0"
python -u mcp_servers\duckdb_server.py

