import logging
from aiogram import Bot, Dispatcher, Router, types
from aiohttp import ClientSession
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
import asyncio

# Настройка логов
logging.basicConfig(level=logging.INFO)

# Базовый URL для взаимодействия с Django API
DJANGO_API_BASE_URL = "http://127.0.0.1:8000/booking/api/"

# Инициализация бота
bot = Bot(token="7858593332:AAGhwrIZJsh3ZkhkfgLZ39Sh1GEG2RhpW80")

# Инициализация хранилища состояний и диспетчера
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Создание роутера для регистрации обработчиков
router = Router()

# Класс состояний для FSM
class BookingState(StatesGroup):
    date = State()
    space = State()
    preferences = State()

@router.message(Command(commands=['start']))
async def start(message: types.Message, state: FSMContext):
    """
    Обработчик команды /start.
    Запуск диалога для бронирования.
    """
    await message.reply("Привет! Укажите дату для бронирования:")
    await state.set_state(BookingState.date)

@router.message(BookingState.date)
async def set_date(message: types.Message, state: FSMContext):
    """
    Обработка ввода даты.
    """
    async with ClientSession() as session:
        async with session.get(f"{DJANGO_API_BASE_URL}check-availability/") as response:
            if response.status == 200:
                spaces = await response.json()
            else:
                spaces = []
    
    await state.update_data(date=message.text)

    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for space in spaces:
        reply_markup.add(types.KeyboardButton(space['name']))

    await message.reply("Выберите пространство:", reply_markup=reply_markup)
    await state.set_state(BookingState.space)

@router.message(BookingState.space)
async def set_space(message: types.Message, state: FSMContext):
    """
    Обработка выбора пространства.
    """
    await state.update_data(space=message.text)
    await message.reply("Укажите ваши предпочтения (например, освещение, звук и т.д.):")
    await state.set_state(BookingState.preferences)

@router.message(BookingState.preferences)
async def set_preferences(message: types.Message, state: FSMContext):
    """
    Обработка предпочтений и завершение бронирования.
    """
    user_data = await state.get_data()
    user_data['preferences'] = message.text

    async with ClientSession() as session:
        async with session.post(f"{DJANGO_API_BASE_URL}create-booking/", json=user_data) as response:
            if response.status == 201:
                await message.reply("Ваше бронирование успешно создано!")
            else:
                await message.reply("Произошла ошибка. Попробуйте снова.")
    
    await state.clear()

# Регистрация роутера в диспетчере
dp.include_router(router)

async def main():
    """
    Запуск бота.
    """
    await dp.start_polling(bot)

# Запуск приложения
if __name__ == "__main__":
    asyncio.run(main())
