#!/usr/bin/env python3
import asyncio
from telegram.ext import Application, CommandHandler, MessageHandler

from config import BOT_CONFIG
from utils.logger import logger
from bot.handlers import BotHandlers
from bot.filters import CustomFilters

class MusicBot:
    def __init__(self):
        self.token = BOT_CONFIG.TOKEN
        self.handlers = BotHandlers()
        self.application = None
    
    async def setup(self):
        """Настройка приложения"""
        self.application = Application.builder().token(self.token).build()
        
        # Регистрация обработчиков
        self.application.add_handler(CommandHandler("start", self.handlers.start_command))
        self.application.add_handler(CommandHandler("help", self.handlers.help_command))
        self.application.add_handler(MessageHandler(
            CustomFilters.music_query(), 
            self.handlers.handle_music_query
        ))
        
        logger.info("Bot setup completed")
    
    async def run(self):
        """Запуск бота"""
        await self.setup()
        
        logger.info("Starting bot...")
        await self.application.run_polling()

async def main():
    bot = MusicBot()
    await bot.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")