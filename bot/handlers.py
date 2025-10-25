from telegram import Update, InputFile
from telegram.ext import ContextTypes
import os

from config import BOT_CONFIG, DOWNLOAD_CONFIG
from utils.logger import logger
from services.searcher import MusicSearcher
from services.downloader import MusicDownloader
from services.file_manager import FileManager

class BotHandlers:
    def __init__(self):
        self.searcher = MusicSearcher()
        self.downloader = MusicDownloader()
        self.file_manager = FileManager()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_text = """
🎵 Добро пожаловать в Music Bot!

Просто напиши название трека или исполнителя, и я найду музыку для тебя!

Примеры:
• "The Weeknd Blinding Lights"
• "Queen Bohemian Rhapsody"
• "Coldplay Adventure Of A Lifetime"
        """
        await update.message.reply_text(welcome_text)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /help"""
        help_text = """
🤖 Помощь по использованию бота:

• Просто напиши название трека или исполнителя
• Бот найдет и отправит аудиофайл
• Максимальный размер файла: 50MB

Если возникли проблемы - попробуй другой запрос или проверь написание.
        """
        await update.message.reply_text(help_text)
    
    async def handle_music_query(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик музыкальных запросов"""
        query = update.message.text.strip()
        
        if len(query) < 2:
            await update.message.reply_text("❌ Запрос слишком короткий")
            return
        
        try:
            # Отправляем статус поиска
            status_msg = await update.message.reply_text("🔍 Ищу музыку...")
            
            # Поиск трека
            track_info = await self.searcher.search_track(query)
            if not track_info:
                await status_msg.edit_text("❌ Трек не найден")
                return
            
            await status_msg.edit_text(f"🎵 Найден: {track_info['title']}\n📥 Скачиваю...")
            
            # Скачивание аудио
            audio_path = await self.downloader.download_audio(query, track_info)
            if not audio_path:
                await status_msg.edit_text("❌ Ошибка при скачивании")
                return
            
            # Проверка размера файла
            file_size = self.file_manager.get_file_size(audio_path)
            if file_size > DOWNLOAD_CONFIG.MAX_FILE_SIZE:
                await status_msg.edit_text("❌ Файл слишком большой для отправки")
                os.unlink(audio_path)
                return
            
            await status_msg.edit_text("📤 Отправляю...")
            
            # Отправка аудио
            with open(audio_path, 'rb') as audio_file:
                await update.message.reply_audio(
                    audio=InputFile(audio_file, filename=f"{track_info['title']}.mp3"),
                    title=track_info['title'],
                    performer=track_info['uploader'],
                    duration=track_info['duration']
                )
            
            await status_msg.delete()
            
            # Очистка временного файла
            try:
                os.unlink(audio_path)
            except:
                pass
                
        except Exception as e:
            logger.error(f"Handler error: {e}")
            await update.message.reply_text("⚠️ Произошла ошибка при обработке запроса")