# Инструкция по выгрузке проекта на GitHub

## Шаг 1: Создание репозитория на GitHub

1. Откройте [GitHub](https://github.com/) и войдите в свой аккаунт
2. Нажмите на кнопку **"+"** в правом верхнем углу → **"New repository"**
3. Заполните форму:
   - **Repository name**: `case_administrator` (или любое другое имя)
   - **Description**: `Telegram bot for chat moderation with Supabase integration`
   - Выберите **Public** или **Private**
   - **НЕ** ставьте галочки на "Initialize this repository with a README" (у нас уже есть README)
4. Нажмите **"Create repository"**

## Шаг 2: Подключение локального репозитория к GitHub

После создания репозитория GitHub покажет вам команды. Выполните следующие команды в терминале:

### Если репозиторий пустой (рекомендуется):

```bash
# Добавьте remote репозиторий (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/case_administrator.git

# Переименуйте ветку в main (если нужно)
git branch -M main

# Выгрузите код на GitHub
git push -u origin main
```

### Альтернативный вариант (если используете SSH):

```bash
git remote add origin git@github.com:YOUR_USERNAME/case_administrator.git
git branch -M main
git push -u origin main
```

## Шаг 3: Проверка

После выполнения команд откройте ваш репозиторий на GitHub и убедитесь, что все файлы загружены.

## Дополнительные команды Git

### Просмотр статуса:
```bash
git status
```

### Просмотр истории коммитов:
```bash
git log --oneline
```

### Добавление изменений и создание нового коммита:
```bash
git add .
git commit -m "Описание изменений"
git push
```

### Просмотр удаленных репозиториев:
```bash
git remote -v
```

## Важные замечания

⚠️ **Безопасность:**
- Файл `.env` **НЕ** попадет в репозиторий (он в `.gitignore`)
- Все секретные данные (токены, пароли) должны быть только в `.env`
- Файл `.env_example` содержит примеры без реальных данных

✅ **Что будет в репозитории:**
- Весь исходный код проекта
- Docker конфигурации
- Документация (README.md, SUPABASE_SETUP.md, MCP_SETUP.md)
- Примеры конфигурации (.env_example)

## Troubleshooting

### Если возникла ошибка аутентификации:

1. Используйте Personal Access Token вместо пароля:
   - GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Создайте новый token с правами `repo`
   - Используйте token как пароль при `git push`

2. Или настройте SSH ключи:
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   # Добавьте публичный ключ в GitHub → Settings → SSH and GPG keys
   ```

### Если нужно изменить URL remote репозитория:

```bash
git remote set-url origin https://github.com/YOUR_USERNAME/case_administrator.git
```

