# Скрипт для открытия/восстановления окна Docker Desktop

Write-Host "=== Открытие Docker Desktop ===" -ForegroundColor Cyan
Write-Host ""

# Проверяем, запущен ли Docker Desktop
$dockerProcesses = Get-Process -Name "Docker Desktop" -ErrorAction SilentlyContinue

if ($dockerProcesses) {
    Write-Host "Docker Desktop уже запущен. Пытаюсь восстановить окно..." -ForegroundColor Yellow
    
    # Пробуем восстановить окно через Win32 API
    Add-Type @"
        using System;
        using System.Runtime.InteropServices;
        public class Win32 {
            [DllImport("user32.dll")]
            public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
            [DllImport("user32.dll")]
            public static extern bool SetForegroundWindow(IntPtr hWnd);
            public const int SW_RESTORE = 9;
            public const int SW_SHOW = 5;
        }
"@
    
    $windowFound = $false
    foreach ($proc in $dockerProcesses) {
        if ($proc.MainWindowHandle -ne [IntPtr]::Zero) {
            [Win32]::ShowWindow($proc.MainWindowHandle, [Win32]::SW_RESTORE)
            [Win32]::SetForegroundWindow($proc.MainWindowHandle)
            Write-Host "Окно Docker Desktop восстановлено! (PID: $($proc.Id))" -ForegroundColor Green
            $windowFound = $true
            break
        }
    }
    
    if (-not $windowFound) {
        Write-Host "Процесс запущен, но окно не найдено." -ForegroundColor Yellow
        Write-Host "Попробуйте:" -ForegroundColor Cyan
        Write-Host "  1. Проверить трей (рядом с часами) - там может быть иконка Docker" -ForegroundColor White
        Write-Host "  2. Нажать Alt+Tab для переключения между окнами" -ForegroundColor White
        Write-Host "  3. Проверить панель задач" -ForegroundColor White
    }
} else {
    Write-Host "Docker Desktop не запущен. Запускаю..." -ForegroundColor Yellow
    
    $dockerPath = "C:\Program Files\Docker\Docker\Docker Desktop.exe"
    if (Test-Path $dockerPath) {
        try {
            Start-Process $dockerPath
            Write-Host "Docker Desktop запускается..." -ForegroundColor Green
            Write-Host "Подождите 10-15 секунд, пока он полностью загрузится." -ForegroundColor Yellow
        } catch {
            Write-Host "Ошибка при запуске: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "Docker Desktop не найден по пути: $dockerPath" -ForegroundColor Red
        Write-Host "Попробуйте запустить его вручную из меню Пуск" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Альтернатива: используйте команды для просмотра логов:" -ForegroundColor Cyan
Write-Host "  docker ps                    - список контейнеров" -ForegroundColor White
Write-Host "  docker logs telegram_moderation_bot -f  - логи бота" -ForegroundColor White

