import os
import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from anthropic import Anthropic

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
OMNIROUTE_BASE_URL = os.getenv('OMNIROUTE_BASE_URL', 'https://api.anthropic.com')

client = Anthropic(
    api_key=ANTHROPIC_API_KEY,
    base_url=OMNIROUTE_BASE_URL
)

user_conversations = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_id = update.effective_user.id
    user_conversations[user_id] = []

    await update.message.reply_text(
        'Привет! Я бот с Claude AI.\n'
        'Просто напиши мне сообщение, и я отвечу.\n\n'
        'Команды:\n'
        '/start - начать заново\n'
        '/clear - очистить историю разговора'
    )

async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Очистка истории разговора"""
    user_id = update.effective_user.id
    user_conversations[user_id] = []
    await update.message.reply_text('История разговора очищена.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка текстовых сообщений"""
    user_id = update.effective_user.id
    user_message = update.message.text

    if user_id not in user_conversations:
        user_conversations[user_id] = []

    user_conversations[user_id].append({
        "role": "user",
        "content": user_message
    })

    await update.message.chat.send_action(action="typing")

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=8096,
            messages=user_conversations[user_id]
        )

        assistant_message = response.content[0].text

        user_conversations[user_id].append({
            "role": "assistant",
            "content": assistant_message
        })

        if len(assistant_message) > 4096:
            for i in range(0, len(assistant_message), 4096):
                await update.message.reply_text(assistant_message[i:i+4096])
        else:
            await update.message.reply_text(assistant_message)

    except Exception as e:
        logger.error(f"Ошибка при обращении к Claude API: {e}")
        await update.message.reply_text(f"Произошла ошибка: {str(e)}")

async def main():
    """Запуск бота"""
    if not TELEGRAM_TOKEN:
        raise ValueError("Не установлен TELEGRAM_BOT_TOKEN")
    if not ANTHROPIC_API_KEY:
        raise ValueError("Не установлен ANTHROPIC_API_KEY")

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("clear", clear))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен...")

    await application.initialize()
    await application.start()
    await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)

    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        await application.updater.stop()
        await application.stop()
        await application.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
