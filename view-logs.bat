@echo off
REM Скрипт для просмотра логов Docker контейнеров
REM Использование: view-logs.bat [bot|db]

if "%1"=="" (
    echo === Просмотр логов Docker контейнеров ===
    echo.
    echo Использование: view-logs.bat [bot^|db]
    echo.
    echo Примеры:
    echo   view-logs.bat bot    - Логи бота
    echo   view-logs.bat db     - Логи базы данных
    echo.
    goto :end
)

if "%1"=="bot" (
    echo Логи бота:
    docker logs telegram_moderation_bot --tail 50
    goto :end
)

if "%1"=="db" (
    echo Логи базы данных:
    docker logs telegram_moderation_db --tail 50
    goto :end
)

:end
echo.
echo Для просмотра логов в реальном времени используйте:
echo   docker logs telegram_moderation_bot -f

