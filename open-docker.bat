@echo off
REM Скрипт для открытия Docker Desktop

echo Попытка открыть Docker Desktop...
echo.

REM Проверяем, запущен ли Docker Desktop
tasklist /FI "IMAGENAME eq Docker Desktop.exe" 2>NUL | find /I /N "Docker Desktop.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Docker Desktop уже запущен, но окно может быть скрыто.
    echo Попробуйте найти его в трее (рядом с часами) или нажать Alt+Tab
    echo.
    echo Перезапускаю Docker Desktop...
    taskkill /F /IM "Docker Desktop.exe" >nul 2>&1
    timeout /t 3 /nobreak >nul
)

REM Запускаем Docker Desktop
start "" "C:\Program Files\Docker\Docker\Docker Desktop.exe"

echo.
echo Docker Desktop запускается...
echo Подождите 10-15 секунд, пока он полностью загрузится.
echo.
echo Если окно не появилось:
echo   1. Проверьте трей (рядом с часами) - там может быть иконка Docker
echo   2. Нажмите Alt+Tab для переключения между окнами
echo   3. Проверьте панель задач - может быть окно свернуто
echo.

timeout /t 15 /nobreak >nul

REM Проверяем, открылось ли окно
tasklist /FI "IMAGENAME eq Docker Desktop.exe" 2>NUL | find /I /N "Docker Desktop.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo Docker Desktop запущен!
) else (
    echo Не удалось запустить Docker Desktop.
    echo Попробуйте запустить его вручную из меню Пуск.
)

pause

