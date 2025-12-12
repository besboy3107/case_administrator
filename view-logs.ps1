# Скрипт для просмотра логов Docker контейнеров
# Использование: .\view-logs.ps1 [bot|db|all] [tail]

param(
    [string]$Service = "bot",
    [int]$Tail = 50
)

Write-Host "=== Просмотр логов Docker контейнеров ===" -ForegroundColor Cyan
Write-Host ""

switch ($Service.ToLower()) {
    "bot" {
        Write-Host "Логи бота (telegram_moderation_bot):" -ForegroundColor Yellow
        docker logs telegram_moderation_bot --tail $Tail
    }
    "db" {
        Write-Host "Логи базы данных (telegram_moderation_db):" -ForegroundColor Yellow
        docker logs telegram_moderation_db --tail $Tail
    }
    "all" {
        Write-Host "Логи бота:" -ForegroundColor Yellow
        docker logs telegram_moderation_bot --tail $Tail
        Write-Host ""
        Write-Host "Логи базы данных:" -ForegroundColor Yellow
        docker logs telegram_moderation_db --tail $Tail
    }
    default {
        Write-Host "Использование: .\view-logs.ps1 [bot|db|all] [tail]" -ForegroundColor Red
        Write-Host "Примеры:" -ForegroundColor Yellow
        Write-Host "  .\view-logs.ps1 bot        # Логи бота (последние 50 строк)"
        Write-Host "  .\view-logs.ps1 bot 100    # Логи бота (последние 100 строк)"
        Write-Host "  .\view-logs.ps1 db         # Логи базы данных"
        Write-Host "  .\view-logs.ps1 all        # Все логи"
    }
}

Write-Host ""
Write-Host "Для просмотра логов в реальном времени используйте:" -ForegroundColor Green
Write-Host "  docker logs telegram_moderation_bot -f" -ForegroundColor White

