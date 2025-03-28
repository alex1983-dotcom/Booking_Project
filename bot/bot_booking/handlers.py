from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from aiogram.filters import Command, StateFilter  # Используем фильтры для команд и состояний
from .keyboards import (
    create_calendar,
    create_month_keyboard,
    create_year_keyboard,
    create_hour_keyboard,
    create_minute_keyboard,
    create_halls_keyboard,
)
from .config import logger, DJANGO_API_BASE_URL

# Создаем маршрутизатор
router = Router()

# === Обработчики ===

# Обработчик команды /start
@router.message(Command(commands=['start']))
async def start_booking(message: types.Message, state: FSMContext):
    """
    Запуск процесса бронирования.
    """
    logger.info("Команда /start получена.")
    await message.reply("Выберите день начала мероприятия:", reply_markup=create_calendar("start"))
    await state.set_state("select_start_day")


# Обработчик выбора дня начала
@router.callback_query(lambda c: c.data.startswith("start_day:"))
async def process_start_day(callback_query: types.CallbackQuery, state: FSMContext):
    day = callback_query.data.split(":")[1]
    logger.info(f"Выбран день начала: {day}")
    await state.update_data(start_day=day)
    await callback_query.message.edit_text("Выберите месяц начала мероприятия:", reply_markup=create_month_keyboard("start"))
    await state.set_state("select_start_month")


# Обработчик выбора месяца начала
@router.callback_query(lambda c: c.data.startswith("start_month:"))
async def process_start_month(callback_query: types.CallbackQuery, state: FSMContext):
    month = callback_query.data.split(":")[1]
    logger.info(f"Выбран месяц начала: {month}")
    await state.update_data(start_month=month)
    await callback_query.message.edit_text("Выберите год начала мероприятия:", reply_markup=create_year_keyboard("start"))
    await state.set_state("select_start_year")


# Обработчик выбора года начала
@router.callback_query(lambda c: c.data.startswith("start_year:"))
async def process_start_year(callback_query: types.CallbackQuery, state: FSMContext):
    year = callback_query.data.split(":")[1]
    logger.info(f"Выбран год начала: {year}")
    await state.update_data(start_year=year)
    await callback_query.message.edit_text("Выберите час начала мероприятия:", reply_markup=create_hour_keyboard("start"))
    await state.set_state("select_start_hour")


# Обработчик выбора часа начала
@router.callback_query(lambda c: c.data.startswith("start_hour:"))
async def process_start_hour(callback_query: types.CallbackQuery, state: FSMContext):
    hour = callback_query.data.split(":")[1]
    logger.info(f"Выбран час начала: {hour}")
    await state.update_data(start_hour=hour)
    await callback_query.message.edit_text("Выберите минуты начала мероприятия:", reply_markup=create_minute_keyboard("start"))
    await state.set_state("select_start_minute")


# Обработчик выбора минут начала
@router.callback_query(lambda c: c.data.startswith("start_minute:"))
async def process_start_minute(callback_query: types.CallbackQuery, state: FSMContext):
    minute = callback_query.data.split(":")[1]
    logger.info(f"Выбраны минуты начала: {minute}")
    await state.update_data(start_minute=minute)
    await callback_query.message.edit_text("Выберите день окончания мероприятия:", reply_markup=create_calendar("end"))
    await state.set_state("select_end_day")


# Обработчик выбора дня окончания
@router.callback_query(lambda c: c.data.startswith("end_day:"))
async def process_end_day(callback_query: types.CallbackQuery, state: FSMContext):
    day = callback_query.data.split(":")[1]
    logger.info(f"Выбран день окончания: {day}")
    await state.update_data(end_day=day)
    await callback_query.message.edit_text("Выберите месяц окончания мероприятия:", reply_markup=create_month_keyboard("end"))
    await state.set_state("select_end_month")


# Обработчик выбора месяца окончания
@router.callback_query(lambda c: c.data.startswith("end_month:"))
async def process_end_month(callback_query: types.CallbackQuery, state: FSMContext):
    month = callback_query.data.split(":")[1]
    logger.info(f"Выбран месяц окончания: {month}")
    await state.update_data(end_month=month)
    await callback_query.message.edit_text("Выберите год окончания мероприятия:", reply_markup=create_year_keyboard("end"))
    await state.set_state("select_end_year")


# Обработчик выбора года окончания
@router.callback_query(lambda c: c.data.startswith("end_year:"))
async def process_end_year(callback_query: types.CallbackQuery, state: FSMContext):
    year = callback_query.data.split(":")[1]
    logger.info(f"Выбран год окончания: {year}")
    await state.update_data(end_year=year)
    await callback_query.message.edit_text("Выберите час окончания мероприятия:", reply_markup=create_hour_keyboard("end"))
    await state.set_state("select_end_hour")


# Обработчик выбора часа окончания
@router.callback_query(lambda c: c.data.startswith("end_hour:"))
async def process_end_hour(callback_query: types.CallbackQuery, state: FSMContext):
    hour = callback_query.data.split(":")[1]
    logger.info(f"Выбран час окончания: {hour}")
    await state.update_data(end_hour=hour)
    await callback_query.message.edit_text("Выберите минуты окончания мероприятия:", reply_markup=create_minute_keyboard("end"))
    await state.set_state("select_end_minute")


# Обработчик выбора минут окончания
@router.callback_query(lambda c: c.data.startswith("end_minute:"))
async def process_end_minute(callback_query: types.CallbackQuery, state: FSMContext):
    minute = callback_query.data.split(":")[1]
    logger.info(f"Выбраны минуты окончания: {minute}")
    await state.update_data(end_minute=minute)
    logger.info(f"Все данные для бронирования: {await state.get_data()}")
    # Здесь можно добавить логику для проверки доступных залов или перехода к следующему шагу.


    # Формируем данные для проверки доступных залов
    user_data = await state.get_data()
    start_datetime = f"{user_data['start_year']}-{user_data['start_month']}-{user_data['start_day']} {user_data['start_hour']}:{user_data['start_minute']}"
    end_datetime = f"{user_data['end_year']}-{user_data['end_month']}-{user_data['end_day']} {user_data['end_hour']}:{user_data['end_minute']}"
    logger.info(f"Начало: {start_datetime}, Окончание: {end_datetime}")

    # Проверяем доступные залы через API
    async with ClientSession() as session:
        async with session.get(f"{DJANGO_API_BASE_URL}check-availability/", params={
            "start": start_datetime,
            "end": end_datetime
        }) as response:
            if response.status == 200:
                response_data = await response.json()
                halls = response_data.get("spaces", [])
                logger.info(f"Доступные залы: {halls}")
                if halls:
                    await callback_query.message.edit_text("Выберите доступный зал:", reply_markup=create_halls_keyboard(halls))
                    await state.set_state("hall_selection")
                else:
                    await callback_query.message.edit_text("Нет доступных залов на указанное время.")
                    await state.clear()
            else:
                logger.error(f"Ошибка API: статус {response.status}")
                await callback_query.message.edit_text("Произошла ошибка при получении данных от сервера.")
                await state.clear()


# Обработчик выбора зала
@router.callback_query(lambda c: c.data.startswith("hall:"))
async def process_hall_selection(callback_query: types.CallbackQuery, state: FSMContext):
    hall_id = callback_query.data.split(":")[1]
    logger.info(f"Выбран зал: {hall_id}")
    await state.update_data(selected_hall=hall_id)
    await callback_query.message.edit_text("Укажите ваши пожелания:")
    await state.set_state("preferences")

# Обработчик завершения бронирования
@router.message(StateFilter("preferences"))  # Используем StateFilter
async def finalize_booking(message: types.Message, state: FSMContext):
    """
    Сбор всех данных и завершение бронирования.
    """
    # Получаем данные от пользователя
    user_data = await state.get_data()
    user_data['preferences'] = message.text.strip() if message.text else "Без предпочтений"
    logger.info(f"Данные для бронирования: {user_data}")

    # Отправляем данные на сервер
    async with ClientSession() as session:
        async with session.post(f"{DJANGO_API_BASE_URL}create-booking/", json=user_data) as response:
            if response.status == 201:
                await message.reply("Ваше бронирование успешно создано!")
                logger.info("Бронирование успешно завершено.")
            else:
                logger.error(f"Ошибка при создании бронирования: {response.status}")
                await message.reply("Произошла ошибка при создании бронирования. Попробуйте ещё раз.")

    await state.clear()

# Обработчик отмены бронирования
@router.callback_query(lambda c: c.data == "cancel")
async def handle_cancel(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработка действия отмены.
    """
    logger.info("Операция отменена пользователем.")
    await state.clear()
    await callback_query.message.edit_text("Операция отменена. Начните заново с /start.")
