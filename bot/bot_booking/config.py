
import logging
from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import os

# Загружаем переменные из файла .env
load_dotenv()

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройки
TOKEN = os.getenv("TOKEN")  # Токен из файла .env
DJANGO_API_BASE_URL = os.getenv("DJANGO_API_BASE_URL")  # Базовый URL API из .env

# Экземпляры бота и хранилища
bot = Bot(token=TOKEN)
storage = MemoryStorage()

# Проверяем, что токен загружен корректно
if not TOKEN:
    logger.error("Токен не найден! Проверьте файл .env.")
