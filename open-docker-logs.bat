@echo off
REM Скрипт для запуска Docker Desktop и просмотра логов

echo === Просмотр логов Docker ===
echo.

REM Проверяем, запущен ли Docker Desktop
tasklist /FI "IMAGENAME eq Docker Desktop.exe" 2>NUL | find /I /N "Docker Desktop.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Docker Desktop уже запущен.
    echo Откройте Docker Desktop и перейдите к контейнеру telegram_moderation_bot
) else (
    echo Docker Desktop не запущен. Пытаюсь запустить...
    start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    echo Docker Desktop запускается. Подождите несколько секунд...
    echo После запуска откройте Docker Desktop и перейдите к контейнеру telegram_moderation_bot
)

echo.
echo Текущие логи бота (последние 20 строк):
echo ----------------------------------------
docker logs telegram_moderation_bot --tail 20

echo.
echo Для просмотра логов в реальном времени используйте:
echo   docker logs telegram_moderation_bot -f

pause

