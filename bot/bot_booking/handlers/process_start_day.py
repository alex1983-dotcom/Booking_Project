from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from ..keyboards import create_month_keyboard, create_year_keyboard, create_hour_keyboard, create_minute_keyboard, create_calendar
from ..config import logger


router = Router()

# Обработчик выбора дня начала
@router.callback_query(lambda c: c.data.startswith("start_day:"))
async def process_start_day(callback_query: types.CallbackQuery, state: FSMContext):
    day = callback_query.data.split(":")[1]
    logger.info(f"Выбран день начала: {day}")
    await state.update_data(start_day=day)
    await callback_query.message.edit_text("Выберите месяц начала мероприятия: 🗓️", reply_markup=create_month_keyboard("start"))
    await state.set_state("select_start_month")


# Обработчик выбора месяца начала
@router.callback_query(lambda c: c.data.startswith("start_month:"))
async def process_start_month(callback_query: types.CallbackQuery, state: FSMContext):
    month = callback_query.data.split(":")[1]
    logger.info(f"Выбран месяц начала: {month}")
    await state.update_data(start_month=month)
    await callback_query.message.edit_text("Выберите год начала мероприятия: 🗓️", reply_markup=create_year_keyboard("start"))
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


# Обработчик выбора минуты начала
@router.callback_query(lambda c: c.data.startswith("start_minute:"))
async def process_start_minute(callback_query: types.CallbackQuery, state: FSMContext):
    minute = callback_query.data.split(":")[1]
    logger.info(f"Выбраны минуты начала: {minute}")
    await state.update_data(start_minute=minute)
    await callback_query.message.edit_text("Выберите день окончания мероприятия:", reply_markup=create_calendar("end"))
    await state.set_state("select_end_day")
