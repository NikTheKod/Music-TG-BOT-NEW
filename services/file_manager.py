import os
import glob
from typing import Optional
from config import DOWNLOAD_CONFIG
from utils.logger import logger
from utils.helpers import generate_file_hash

class FileManager:
    def __init__(self):
        self.temp_dir = DOWNLOAD_CONFIG.TEMP_DIR
    
    def find_downloaded_file(self, query: str) -> Optional[str]:
        """Поиск уже скачанного файла по запросу"""
        try:
            file_hash = generate_file_hash(query)
            pattern = os.path.join(self.temp_dir, f"*{file_hash}*.mp3")
            files = glob.glob(pattern)
            return files[0] if files else None
        except Exception as e:
            logger.error(f"Error finding file: {e}")
            return None
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """Очистка старых файлов"""
        try:
            import time
            current_time = time.time()
            for filename in os.listdir(self.temp_dir):
                filepath = os.path.join(self.temp_dir, filename)
                if os.path.isfile(filepath):
                    file_age = current_time - os.path.getctime(filepath)
                    if file_age > max_age_hours * 3600:
                        os.remove(filepath)
                        logger.info(f"Removed old file: {filename}")
        except Exception as e:
            logger.error(f"Error cleaning up files: {e}")
    
    def get_file_size(self, filepath: str) -> int:
        """Получение размера файла"""
        return os.path.getsize(filepath)