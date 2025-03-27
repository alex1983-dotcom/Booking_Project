import logging
from aiogram import Bot, Dispatcher, Router, types
from aiohttp import ClientSession
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

# === Настройка логирования ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Настройка бота ===
DJANGO_API_BASE_URL = "http://127.0.0.1:8000/booking/api/"
bot = Bot(token="7858593332:AAGhwrIZJsh3ZkhkfgLZ39Sh1GEG2RhpW80")
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()

# === Определение состояний FSM ===
class BookingState(StatesGroup):
    select_start_day = State()
    select_start_month = State()
    select_start_year = State()
    select_start_hour = State()
    select_start_minute = State()
    select_end_day = State()
    select_end_month = State()
    select_end_year = State()
    select_end_hour = State()
    select_end_minute = State()
    hall_selection = State()
    preferences = State()

# === Функции для создания клавиатур ===
def create_calendar():
    """Клавиатура с днями месяца."""
    buttons = [
        [InlineKeyboardButton(text=str(day), callback_data=f"day:{day}") for day in range(i, i+7)]
        for i in range(1, 32, 7)
    ]
    buttons.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_month_keyboard():
    """Клавиатура с месяцами."""
    months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
              'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
    buttons = [
        [InlineKeyboardButton(text=month, callback_data=f"month:{i+1}") for i, month in enumerate(months[j:j+4])]
        for j in range(0, 12, 4)
    ]
    buttons.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_year_keyboard():
    """Клавиатура для выбора года."""
    buttons = [[InlineKeyboardButton(text=str(year), callback_data=f"year:{year}") for year in range(2025, 2031)]]
    buttons.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_hour_keyboard():
    """Клавиатура для выбора часа."""
    buttons = [
        [InlineKeyboardButton(text=f"{hour:02}", callback_data=f"hour:{hour}") for hour in range(i, i+3)]
        for i in range(8, 23, 3)
    ]
    buttons.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_minute_keyboard():
    """Клавиатура для выбора минут."""
    buttons = [
        [InlineKeyboardButton(text=f"{minute:02}", callback_data=f"minute:{minute}") for minute in range(0, 60, 15)]
    ]
    buttons.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def create_halls_keyboard(halls):
    """Клавиатура с доступными залами."""
    buttons = [
        [InlineKeyboardButton(text=hall['name'], callback_data=f"hall:{hall['id']}")] for hall in halls
    ]
    buttons.append([InlineKeyboardButton(text="Отмена", callback_data="cancel")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# === Основные обработчики ===
@router.message(Command(commands=['start']))
async def start_booking(message: types.Message, state: FSMContext):
    logger.info("Команда /start получена. Начинаем процесс бронирования.")
    await message.reply("Выберите день начала мероприятия:", reply_markup=create_calendar())
    await state.set_state(BookingState.select_start_day)

@router.callback_query(lambda c: c.data and c.data.startswith("day:"))
async def process_start_day(callback_query: types.CallbackQuery, state: FSMContext):
    day = callback_query.data.split(":")[1]
    logger.info(f"Выбран день начала: {day}")
    await state.update_data(start_day=day)
    await callback_query.message.edit_text("Выберите месяц начала мероприятия:", reply_markup=create_month_keyboard())
    await state.set_state(BookingState.select_start_month)

@router.callback_query(lambda c: c.data and c.data.startswith("month:"))
async def process_start_month(callback_query: types.CallbackQuery, state: FSMContext):
    month = callback_query.data.split(":")[1]
    logger.info(f"Выбран месяц начала: {month}")
    await state.update_data(start_month=month)
    await callback_query.message.edit_text("Выберите год начала мероприятия:", reply_markup=create_year_keyboard())
    await state.set_state(BookingState.select_start_year)

@router.callback_query(lambda c: c.data and c.data.startswith("year:"))
async def process_start_year(callback_query: types.CallbackQuery, state: FSMContext):
    year = callback_query.data.split(":")[1]
    logger.info(f"Выбран год начала: {year}")
    await state.update_data(start_year=year)
    await callback_query.message.edit_text("Выберите час начала мероприятия:", reply_markup=create_hour_keyboard())
    await state.set_state(BookingState.select_start_hour)

@router.callback_query(lambda c: c.data and c.data.startswith("hour:"))
async def process_start_hour(callback_query: types.CallbackQuery, state: FSMContext):
    hour = callback_query.data.split(":")[1]
    logger.info(f"Выбран час начала: {hour}")
    await state.update_data(start_hour=hour)
    await callback_query.message.edit_text("Выберите минуты начала мероприятия:", reply_markup=create_minute_keyboard())
    await state.set_state(BookingState.select_start_minute)

@router.callback_query(lambda c: c.data and c.data.startswith("minute:"))
async def process_start_minute(callback_query: types.CallbackQuery, state: FSMContext):
    minute = callback_query.data.split(":")[1]
    logger.info(f"Выбраны минуты начала: {minute}")
    await state.update_data(start_minute=minute)
    await callback_query.message.edit_text("Выберите день окончания мероприятия:", reply_markup=create_calendar())
    await state.set_state(BookingState.select_end_day)

@router.callback_query(lambda c: c.data and c.data.startswith("day:"))
async def process_end_day(callback_query: types.CallbackQuery, state: FSMContext):
    end_day = callback_query.data.split(":")[1]
    logger.info(f"Выбран день окончания: {end_day}")
    user_data = await state.get_data()
    start_datetime = f"{user_data['start_year']}-{user_data['start_month']}-{user_data['start_day']} {user_data['start_hour']}:{user_data['start_minute']}"
    end_datetime = f"{user_data['start_year']}-{user_data['start_month']}-{end_day} {user_data['start_hour']}:{user_data['start_minute']}"
    logger.info(f"Сформировано время начала: {start_datetime}, время окончания: {end_datetime}")

    async with ClientSession() as session:
        async with session.get(f"{DJANGO_API_BASE_URL}check-availability/", params={
            "start": start_datetime,
            "end": end_datetime
        }) as response:
            if response.status == 200:
                halls = await response.json()
                if halls:
                    logger.info(f"Доступные залы: {halls}")
                    await callback_query.message.edit_text("Выберите доступный зал:", reply_markup=create_halls_keyboard(halls))
                    await state.set_state(BookingState.hall_selection)
                else:
                    logger.info("Нет доступных залов на выбранное время.")
                    await callback_query.message.edit_text("Нет доступных залов на выбранное время.")
                    await state.clear()
            else:
                logger.error(f"Ошибка API: {response.status}")
                await callback_query.message.edit_text("Произошла ошибка при проверке доступных залов.")
                await state.clear()

@router.callback_query(lambda c: c.data.startswith("hall:"))
async def process_hall_selection(callback_query: types.CallbackQuery, state: FSMContext):
    hall_id = callback_query.data.split(":")[1]
    logger.info(f"Выбран зал: {hall_id}")
    await state.update_data(selected_hall=hall_id)
    await callback_query.message.edit_text("Укажите пожелания для вашего мероприятия (например, освещение, звук):")
    await state.set_state(BookingState.preferences)

@router.callback_query(lambda c: c.data == "cancel")
async def handle_cancel(callback_query: types.CallbackQuery, state: FSMContext):
    logger.info("Операция отменена пользователем.")
    await state.clear()
    await callback_query.message.edit_text("Операция отменена. Вы можете начать заново, отправив /start.")

@router.message(BookingState.preferences)
async def finalize_booking(message: types.Message, state: FSMContext):
    """
    Сбор всех данных и завершение бронирования.
    """
    # Получаем данные, которые были собраны на предыдущих шагах
    user_data = await state.get_data()

    # Формируем информацию о бронировании для ответа пользователю
    await message.reply(
        f"Ваше бронирование:\n"
        f"Начало: {user_data['start_day']}-{user_data['start_month']}-{user_data['start_year']} {user_data['start_hour']}:{user_data['start_minute']}\n"
        f"Конец: {user_data['end_day']}-{user_data['end_month']}-{user_data['end_year']} {user_data['end_hour']}:{user_data['end_minute']}\n"
        f"Укажите ваши пожелания или дополнительные требования:"
    )

    # Ожидаем ввода пожеланий от пользователя
    user_data['preferences'] = message.text

    # Отправляем данные о бронировании на сервер Django API
    async with ClientSession() as session:
        async with session.post(f"{DJANGO_API_BASE_URL}create-booking/", json=user_data) as response:
            if response.status == 201:
                await message.reply("Ваше бронирование успешно создано!")
            else:
                await message.reply("Произошла ошибка при создании бронирования. Попробуйте ещё раз.")

    # Сбрасываем состояние FSM
    await state.clear()


# Запуск бота
dp.include_router(router)

async def main():
    """
    Основная функция запуска бота.
    """
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
