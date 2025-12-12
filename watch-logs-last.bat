@echo off
REM Скрипт для просмотра последних логов

title Последние логи Telegram бота
color 0B

echo ========================================
echo   ПОСЛЕДНИЕ ЛОГИ TELEGRAM БОТА
echo ========================================
echo.

docker logs telegram_moderation_bot --tail 100

echo.
echo ========================================
echo Для просмотра в реальном времени запустите: watch-logs.bat
echo ========================================
echo.

pause

