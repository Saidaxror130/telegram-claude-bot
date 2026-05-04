# Telegram Claude Bot

Telegram бот, который использует Claude API для общения.

## Установка

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте бота в Telegram через [@BotFather](https://t.me/botfather):
   - Отправьте команду `/newbot`
   - Следуйте инструкциям
   - Сохраните полученный токен

3. Получите API ключ от Anthropic или настройте Omniroute:
   - Для Anthropic: зайдите на https://console.anthropic.com/
   - Для Omniroute: используйте свой локальный endpoint

4. Создайте файл `.env` в корне проекта:
```
TELEGRAM_BOT_TOKEN=ваш_токен_от_botfather
ANTHROPIC_API_KEY=ваш_ключ
OMNIROUTE_BASE_URL=http://your-omniroute-url/v1
```

**Примечание для Omniroute:** Если используете локальный Omniroute (`http://localhost:20128/v1`), вам нужно развернуть Omniroute на публичном сервере или использовать туннель (ngrok, cloudflare tunnel), так как Railway не может подключиться к вашему localhost.

## Запуск

```bash
python bot.py
```

## Команды бота

- `/start` - начать разговор
- `/clear` - очистить историю разговора

## Возможности

- Сохраняет историю разговора для каждого пользователя
- Поддерживает длинные ответы (автоматически разбивает на части)
- Использует Claude Sonnet 4.6
