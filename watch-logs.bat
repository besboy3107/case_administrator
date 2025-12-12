@echo off
REM Простой скрипт для просмотра логов в реальном времени
REM Двойной клик по файлу откроет логи бота

title Логи Telegram бота
color 0A

echo ========================================
echo   ЛОГИ TELEGRAM БОТА (в реальном времени)
echo ========================================
echo.
echo Нажмите Ctrl+C для выхода
echo.
echo ========================================
echo.

docker logs telegram_moderation_bot -f

pause

