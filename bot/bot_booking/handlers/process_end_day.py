from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from ..keyboards import create_calendar, create_month_keyboard, create_year_keyboard, create_hour_keyboard, create_minute_keyboard
from ..config import logger

router = Router()

# Обработчики выбора даты окончания
@router.callback_query(lambda c: c.data.startswith("end_day:"))
async def process_end_day(callback_query: types.CallbackQuery, state: FSMContext):
    day = callback_query.data.split(":")[1]
    logger.info(f"Выбран день окончания: {day}")
    await state.update_data(end_day=day)
    await callback_query.message.edit_text("Выберите месяц окончания мероприятия:", reply_markup=create_month_keyboard("end"))
    await state.set_state("select_end_month")


@router.callback_query(lambda c: c.data.startswith("end_month:"))
async def process_end_month(callback_query: types.CallbackQuery, state: FSMContext):
    month = callback_query.data.split(":")[1]
    logger.info(f"Выбран месяц окончания: {month}")
    await state.update_data(end_month=month)
    await callback_query.message.edit_text("Выберите год окончания мероприятия:", reply_markup=create_year_keyboard("end"))
    await state.set_state("select_end_year")


@router.callback_query(lambda c: c.data.startswith("end_year:"))
async def process_end_year(callback_query: types.CallbackQuery, state: FSMContext):
    year = callback_query.data.split(":")[1]
    logger.info(f"Выбран год окончания: {year}")
    await state.update_data(end_year=year)
    await callback_query.message.edit_text("Выберите час окончания мероприятия:", reply_markup=create_hour_keyboard("end"))
    await state.set_state("select_end_hour")


@router.callback_query(lambda c: c.data.startswith("end_hour:"))
async def process_end_hour(callback_query: types.CallbackQuery, state: FSMContext):
    hour = callback_query.data.split(":")[1]
    logger.info(f"Выбран час окончания: {hour}")
    await state.update_data(end_hour=hour)
    await callback_query.message.edit_text("Выберите минуты окончания мероприятия:", reply_markup=create_minute_keyboard("end"))
    await state.set_state("select_end_minute")


@router.callback_query(lambda c: c.data.startswith("end_minute:"))
async def process_end_minute(callback_query: types.CallbackQuery, state: FSMContext):
    minute = callback_query.data.split(":")[1]
    logger.info(f"Выбраны минуты окончания: {minute}")
    await state.update_data(end_minute=minute)
    await callback_query.message.edit_text("Введите количество гостей:")
    await state.set_state("enter_guests")
