import yt_dlp
import os
from typing import Optional
from config import YDL_CONFIG, DOWNLOAD_CONFIG
from utils.logger import logger
from utils.helpers import run_async, generate_file_hash, sanitize_filename
from .file_manager import FileManager

class MusicDownloader:
    def __init__(self):
        self.ydl_opts = YDL_CONFIG.YDL_OPTIONS
        self.file_manager = FileManager()
    
    async def download_audio(self, query: str, track_info: dict) -> Optional[str]:
        """Скачивание аудио по информации о треке"""
        try:
            # Проверяем, нет ли уже скачанного файла
            cached_file = self.file_manager.find_downloaded_file(query)
            if cached_file:
                logger.info(f"Using cached file for: {query}")
                return cached_file
            
            # Скачиваем новый файл
            url = track_info['url']
            file_hash = generate_file_hash(query)
            safe_title = sanitize_filename(track_info['title'])
            
            # Модифицируем опции для конкретного файла
            download_opts = self.ydl_opts.copy()
            download_opts['outtmpl'] = os.path.join(
                DOWNLOAD_CONFIG.TEMP_DIR, 
                f'{safe_title}_{file_hash}.%(ext)s'
            )
            
            with yt_dlp.YoutubeDL(download_opts) as ydl:
                await run_async(ydl.download, [url])
            
            # Ищем скачанный файл
            downloaded_file = self.file_manager.find_downloaded_file(query)
            if downloaded_file:
                logger.info(f"Successfully downloaded: {downloaded_file}")
                return downloaded_file
            else:
                logger.error("Downloaded file not found")
                return None
                
        except Exception as e:
            logger.error(f"Download error for '{query}': {e}")
            return None
