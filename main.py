#!/usr/bin/env python3
import asyncio
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Импорт handlers после настройки логирования
from bot.handlers import BotHandlers

async def main():
    """Основная функция запуска бота"""
    try:
        # Токен бота
        TOKEN = "8232564183:AAGXLqP8WH2bsDFCZzsP_JtmXqh6Ie5DV3k"
        
        # Создаем приложение
        application = Application.builder().token(TOKEN).build()
        
        # Инициализируем обработчики
        bot_handlers = BotHandlers()
        
        # Регистрируем обработчики
        application.add_handler(CommandHandler("start", bot_handlers.start_command))
        application.add_handler(CommandHandler("help", bot_handlers.help_command))
        application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND, 
            bot_handlers.handle_search_query
        ))
        application.add_handler(CallbackQueryHandler(
            bot_handlers.handle_callback_query
        ))
        
        # Запускаем бота
        logger.info("🎵 Music Bot is starting...")
        print("Бот запускается...")
        
        await application.run_polling()
        
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())