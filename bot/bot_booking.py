import logging
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiohttp import ClientSession
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# Настройка бота и API
API_TOKEN = "7858593332:AAGhwrIZJsh3ZkhkfgLZ39Sh1GEG2RhpW80"
API_URL = "http://127.0.0.1:8000/booking/api/"

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

class BookingState(StatesGroup):
    """
    Класс для управления состояниями диалога.
    """
    date = State()  # Состояние: выбор даты
    space = State()  # Состояние: выбор пространства
    preferences = State()  # Состояние: ввод предпочтений

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """
    Обработчик команды /start.
    """
    await message.reply("Привет! Для начала выберите дату для бронирования:")
    await BookingState.date.set()

@dp.message_handler(state=BookingState.date)
async def set_date(message: types.Message, state: FSMContext):
    """
    Обработка ввода даты.
    """
    async with ClientSession() as session:
        async with session.get(f"{API_URL}check-availability/") as response:
            spaces = await response.json()
    
    await state.update_data(date=message.text)
    
    reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for space in spaces:
        reply_markup.add(types.KeyboardButton(space['name']))
    
    await message.reply("Выберите пространство:", reply_markup=reply_markup)
    await BookingState.space.set()

@dp.message_handler(state=BookingState.space)
async def set_space(message: types.Message, state: FSMContext):
    """
    Обработка выбора пространства.
    """
    await state.update_data(space=message.text)
    await message.reply("Укажите ваши предпочтения (например, освещение, звук и т.д.):")
    await BookingState.preferences.set()

@dp.message_handler(state=BookingState.preferences)
async def set_preferences(message: types.Message, state: FSMContext):
    """
    Обработка предпочтений и создание бронирования.
    """
    user_data = await state.get_data()
    user_data['preferences'] = message.text

    async with ClientSession() as session:
        async with session.post(f"{API_URL}create-booking/", json=user_data) as response:
            if response.status == 201:
                await message.reply("Ваше бронирование успешно создано!")
            else:
                await message.reply("Произошла ошибка. Попробуйте снова.")
    
    await state.finish()

# Запуск
if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
