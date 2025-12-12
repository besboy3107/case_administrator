# PowerShell скрипт для запуска DuckDB MCP сервера
# Решает проблему с кириллицей в путях

$ErrorActionPreference = "Stop"

# Определяем директорию скрипта
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Переходим в директорию проекта
Set-Location $scriptDir

# Запускаем Python скрипт с правильной кодировкой
$env:PYTHONIOENCODING = "utf-8"
python -u run_duckdb_mcp.py

