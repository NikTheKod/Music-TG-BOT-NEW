import os
from dataclasses import dataclass

@dataclass
class BotConfig:
    TOKEN: str = "8232564183:AAGXLqP8WH2bsDFCZzsP_JtmXqh6Ie5DV3k"
    ADMIN_IDS: list = None
    
    def __post_init__(self):
        if self.ADMIN_IDS is None:
            self.ADMIN_IDS = [123456789]  # Ваш ID

@dataclass
class DownloadConfig:
    MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50MB
    TEMP_DIR: str = "temp"
    SUPPORTED_FORMATS: list = None
    
    def __post_init__(self):
        if self.SUPPORTED_FORMATS is None:
            self.SUPPORTED_FORMATS = ['mp3', 'm4a']
        
        # Создаем временную директорию
        os.makedirs(self.TEMP_DIR, exist_ok=True)

@dataclass
class YDLConfig:
    YDL_OPTIONS: dict = None
    
    def __post_init__(self):
        if self.YDL_OPTIONS is None:
            self.YDL_OPTIONS = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': 'temp/%(title).100s.%(ext)s',
                'quiet': True,
            }

# Инициализация конфигов
BOT_CONFIG = BotConfig()
DOWNLOAD_CONFIG = DownloadConfig()
YDL_CONFIG = YDLConfig()