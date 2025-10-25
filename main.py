#!/usr/bin/env python3
import asyncio
import signal
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler

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
        try:
            self.application = Application.builder().token(self.token).build()
            
            # Регистрация обработчиков
            self.application.add_handler(CommandHandler("start", self.handlers.start_command))
            self.application.add_handler(CommandHandler("help", self.handlers.help_command))
            self.application.add_handler(MessageHandler(
                CustomFilters.music_query(), 
                self.handlers.handle_search_query
            ))
            self.application.add_handler(CallbackQueryHandler(
                self.handlers.handle_callback_query
            ))
            
            logger.info("Bot setup completed")
            return True
        except Exception as e:
            logger.error(f"Setup error: {e}")
            return False
    
    async def run(self):
        """Запуск бота"""
        if not await self.setup():
            return
        
        logger.info("Starting bot polling...")
        
        try:
            # Правильный запуск для версии 20.x
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            
            # Ожидание остановки
            stop_event = asyncio.Event()
            await stop_event.wait()
            
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Fatal error: {e}")
        finally:
            # Корректное завершение
            await self.application.stop()
            await self.application.shutdown()

async def main():
    bot = MusicBot()
    await bot.run()

if __name__ == "__main__":
    # Простой запуск
    asyncio.run(main())