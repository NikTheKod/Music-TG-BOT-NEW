from telegram.ext import filters

class CustomFilters:
    """Кастомные фильтры для бота"""
    
    @staticmethod
    def music_query():
        """Фильтр для музыкальных запросов"""
        return filters.TEXT & ~filters.COMMAND
    
    @staticmethod
    def admin_only(admin_ids: list):
        """Фильтр только для администраторов"""
        return filters.User(user_id=admin_ids)
