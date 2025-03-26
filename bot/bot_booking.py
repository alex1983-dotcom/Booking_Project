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
    start_date = State()
    end_date = State()
    space = State()
    preferences = State()

@router.message(Command(commands=['start']))
async def start(message: types.Message, state: FSMContext):
    """
    Обработчик команды /start.
    Запуск диалога для бронирования.
    """
    await message.reply("Привет! Укажите дату и время начала мероприятия (в формате YYYY-MM-DD HH:MM):")
    await state.set_state(BookingState.start_date)

@router.message(BookingState.start_date)
async def set_start_date(message: types.Message, state: FSMContext):
    """
    Обработка ввода даты начала.
    """
    await state.update_data(start_date=message.text)  # Сохраняем дату начала
    await message.reply("Укажите дату и время окончания мероприятия (в формате YYYY-MM-DD HH:MM):")
    await state.set_state(BookingState.end_date)

@router.message(BookingState.end_date)
async def set_end_date(message: types.Message, state: FSMContext):
    """
    Обработка ввода даты окончания.
    """
    await state.update_data(end_date=message.text)  # Сохраняем дату окончания

    async with ClientSession() as session:
        async with session.get(f"{DJANGO_API_BASE_URL}check-availability/") as response:
            if response.status == 200:
                spaces = await response.json()
            else:
                spaces = []  # Если запрос не удался, оставляем список пустым
    
    # Формируем кнопки для клавиатуры
    buttons = [[types.KeyboardButton(text=space['name'])] for space in spaces]
    reply_markup = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

    await message.reply("Выберите пространство:", reply_markup=reply_markup)
    await state.set_state(BookingState.space)

@router.message(BookingState.space)
async def set_space(message: types.Message, state: FSMContext):
    """
    Обработка выбора пространства.
    """
    await state.update_data(space=message.text)  # Сохраняем выбранное пространство
    await message.reply("Укажите ваши предпочтения (например, освещение, звук и т.д.):")
    await state.set_state(BookingState.preferences)

@router.message(BookingState.preferences)
async def set_preferences(message: types.Message, state: FSMContext):
    """
    Обработка предпочтений и завершение бронирования.
    """
    user_data = await state.get_data()  # Получаем данные из текущего состояния
    user_data['preferences'] = message.text  # Сохраняем введенные предпочтения

    async with ClientSession() as session:
        async with session.post(f"{DJANGO_API_BASE_URL}create-booking/", json=user_data) as response:
            if response.status == 201:
                await message.reply("Ваше бронирование успешно создано!")
            else:
                await message.reply("Произошла ошибка. Попробуйте снова.")
    
    await state.clear()  # Очищаем все состояния после завершения

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

