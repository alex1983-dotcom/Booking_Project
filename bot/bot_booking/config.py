import logging
from aiogram import Bot
from aiogram.fsm.storage.memory import MemoryStorage

# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройки
TOKEN = "7858593332:AAGhwrIZJsh3ZkhkfgLZ39Sh1GEG2RhpW80"  # Ваш токен
DJANGO_API_BASE_URL = "http://127.0.0.1:8000/api/booking/"



# Экземпляры бота и хранилища
bot = Bot(token=TOKEN)
storage = MemoryStorage()
