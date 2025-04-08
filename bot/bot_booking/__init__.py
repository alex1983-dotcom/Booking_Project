# Импорт настроек
from .config import bot, storage, logger, DJANGO_API_BASE_URL
from .handlers import routers
from .utils import some_helper_function  

# Импорт клавиатур
from .keyboards import (
    create_calendar,
    create_month_keyboard,
    create_year_keyboard,
    create_hour_keyboard,
    create_minute_keyboard,
    create_halls_keyboard,
    create_call_time_keyboard
)

# Экспортируем все зависимости
__all__ = [
    "bot",
    "storage",
    "logger",
    "DJANGO_API_BASE_URL",
    "create_calendar",
    "create_month_keyboard",
    "create_year_keyboard",
    "create_hour_keyboard",
    "create_minute_keyboard",
    "create_halls_keyboard",
    "routers",
    "some_helper_function",
    "create_call_time_keyboard"  
]
