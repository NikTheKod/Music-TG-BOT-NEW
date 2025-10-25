import os
import hashlib
import asyncio
from typing import Optional

def generate_file_hash(query: str) -> str:
    """Генерация хеша для кэширования"""
    return hashlib.md5(query.encode()).hexdigest()

def sanitize_filename(filename: str) -> str:
    """Очистка имени файла от недопустимых символов"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename[:100]  # Ограничение длины

async def run_async(func, *args):
    """Запуск синхронной функции в асинхронном режиме"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func, *args)
