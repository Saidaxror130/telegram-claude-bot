# Деплой на Railway

## Шаги для деплоя:

1. **Создай репозиторий на GitHub:**
   ```bash
   cd C:\Users\SVOY\telegram-claude-bot
   git init
   git add .
   git commit -m "Initial commit: Telegram Claude bot"
   git branch -M main
   git remote add origin https://github.com/твой-username/telegram-claude-bot.git
   git push -u origin main
   ```

2. **Зайди на Railway:**
   - Перейди на https://railway.app/
   - Войди через GitHub
   - Нажми "New Project"
   - Выбери "Deploy from GitHub repo"
   - Выбери свой репозиторий `telegram-claude-bot`

3. **Добавь переменные окружения в Railway:**
   - В проекте перейди в раздел "Variables"
   - Добавь две переменные:
     - `TELEGRAM_BOT_TOKEN` = твой токен от @BotFather
     - `ANTHROPIC_API_KEY` = твой API ключ от Anthropic

4. **Деплой:**
   - Railway автоматически задеплоит бота
   - Проверь логи, чтобы убедиться что бот запустился
   - Найди в логах сообщение "Бот запущен..."

5. **Тестирование:**
   - Открой Telegram
   - Найди своего бота
   - Отправь команду `/start`
   - Попробуй написать сообщение

## Альтернатива: деплой напрямую через Railway CLI

```bash
npm install -g @railway/cli
railway login
railway init
railway up
railway variables set TELEGRAM_BOT_TOKEN=твой_токен
railway variables set ANTHROPIC_API_KEY=твой_ключ
```

## Проверка работы

После деплоя бот должен:
- Отвечать на команду `/start`
- Отвечать на текстовые сообщения через Claude API
- Сохранять историю разговора для каждого пользователя
- Поддерживать команду `/clear` для очистки истории
