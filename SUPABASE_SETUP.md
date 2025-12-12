# Настройка подключения к Supabase

## Как получить данные для подключения:

1. Войдите в ваш проект на [Supabase](https://supabase.com/)
2. Перейдите в **Project Settings** → **Database**
3. Найдите раздел **Connection string** или **Connection pooling**

### Параметры подключения:

- **DB_HOST**: Хост из connection string (например: `db.xxxxxxxxxxxxx.supabase.co`)
- **DB_PORT**: Обычно `5432` для прямого подключения или `6543` для connection pooling
- **DB_NAME**: Обычно `postgres`
- **DB_USER**: Обычно `postgres` (или ваш пользователь из connection string)
- **DB_PASSWORD**: Пароль базы данных (можно найти в Project Settings → Database → Database password)

### Пример connection string из Supabase:
```
postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
```

### Для использования connection pooling (рекомендуется):
- Используйте порт `6543` вместо `5432`
- Хост будет тот же самый

## Обновление .env файла:

Откройте файл `.env` и обновите следующие строки:

```env
DB_HOST=db.xxxxxxxxxxxxx.supabase.co
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=ваш_пароль_из_supabase
```

## Создание таблиц:

После первого подключения бот автоматически создаст необходимые таблицы в базе данных.

## Проверка подключения:

После запуска контейнера проверьте логи:
```bash
docker logs telegram_moderation_bot
```

Если подключение успешно, вы увидите:
```
Успешное подключение к базе данных
Таблицы базы данных проверены/созданы
```

