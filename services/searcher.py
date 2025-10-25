import yt_dlp
from typing import Optional, Dict
from config import YDL_CONFIG
from utils.logger import logger
from utils.helpers import run_async

class MusicSearcher:
    def __init__(self):
        self.ydl_opts = YDL_CONFIG.YDL_OPTIONS
    
    async def search_track(self, query: str) -> Optional[Dict]:
        """Поиск трека по запросу"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Используем ytsearch для поиска на YouTube
                search_query = f"ytsearch:{query}"
                info = await run_async(ydl.extract_info, search_query, download=False)
                
                if not info or 'entries' not in info or not info['entries']:
                    return None
                
                # Берем первый результат
                track_info = info['entries'][0]
                
                return {
                    'url': track_info['webpage_url'],
                    'title': track_info.get('title', 'Unknown'),
                    'duration': track_info.get('duration', 0),
                    'uploader': track_info.get('uploader', 'Unknown'),
                    'thumbnail': track_info.get('thumbnail')
                }
                
        except Exception as e:
            logger.error(f"Search error for '{query}': {e}")
            return None