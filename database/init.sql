-- Скрипт инициализации базы данных для Telegram-бота модерации
-- Этот скрипт выполняется автоматически при первом подключении бота к БД

-- Таблица для хранения всех действий бота
CREATE TABLE IF NOT EXISTS bot_actions (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    chat_id BIGINT NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    message_text TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    additional_data JSONB
);

-- Индексы для оптимизации запросов
CREATE INDEX IF NOT EXISTS idx_user_id ON bot_actions(user_id);
CREATE INDEX IF NOT EXISTS idx_chat_id ON bot_actions(chat_id);
CREATE INDEX IF NOT EXISTS idx_timestamp ON bot_actions(timestamp);
CREATE INDEX IF NOT EXISTS idx_action_type ON bot_actions(action_type);

-- Комментарии к таблице и полям
COMMENT ON TABLE bot_actions IS 'Таблица для хранения истории действий бота модерации';
COMMENT ON COLUMN bot_actions.id IS 'Уникальный идентификатор записи';
COMMENT ON COLUMN bot_actions.user_id IS 'ID пользователя Telegram';
COMMENT ON COLUMN bot_actions.chat_id IS 'ID чата, в котором произошло действие';
COMMENT ON COLUMN bot_actions.action_type IS 'Тип действия: message_received, message_deleted, error, bot_removed';
COMMENT ON COLUMN bot_actions.message_text IS 'Текст сообщения';
COMMENT ON COLUMN bot_actions.timestamp IS 'Время действия';
COMMENT ON COLUMN bot_actions.additional_data IS 'Дополнительные данные в формате JSON';

