from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from ..keyboards import create_month_keyboard, create_year_keyboard, create_hour_keyboard, create_minute_keyboard
from ..config import logger

router = Router()

# Обработчик выбора дня начала
@router.callback_query(lambda c: c.data.startswith("start_day:"))
async def process_start_day(callback_query: types.CallbackQuery, state: FSMContext):
    day = callback_query.data.split(":")[1]
    # Проверка на валидность дня
    if not day.isdigit() or int(day) not in range(1, 32):
        await callback_query.answer("Некорректный день. Выберите в диапазоне от 1 до 31.", show_alert=True)
        logger.error(f"Некорректный день: {day}")
        return
    logger.info(f"Выбран день начала: {day}")
    await state.update_data(start_day=day)  # Сохраняем день в FSM
    await callback_query.message.edit_text(
        "Выберите месяц начала мероприятия:",
        reply_markup=create_month_keyboard("start")  # Переход к выбору месяца
    )
    await state.set_state("select_start_month")  # Устанавливаем состояние

# Обработчик выбора месяца начала
@router.callback_query(lambda c: c.data.startswith("start_month:"))
async def process_start_month(callback_query: types.CallbackQuery, state: FSMContext):
    month = callback_query.data.split(":")[1]
    # Проверка на валидность месяца
    if not month.isdigit() or int(month) not in range(1, 13):
        await callback_query.answer("Некорректный месяц. Выберите в диапазоне от 1 до 12.", show_alert=True)
        logger.error(f"Некорректный месяц: {month}")
        return
    logger.info(f"Выбран месяц начала: {month}")
    await state.update_data(start_month=month)  # Сохраняем месяц в FSM
    await callback_query.message.edit_text(
        "Выберите год начала мероприятия:",
        reply_markup=create_year_keyboard("start")  # Переход к выбору года
    )
    await state.set_state("select_start_year")  # Устанавливаем состояние

# Обработчик выбора года начала
@router.callback_query(lambda c: c.data.startswith("start_year:"))
async def process_start_year(callback_query: types.CallbackQuery, state: FSMContext):
    year = callback_query.data.split(":")[1]
    # Проверка на валидность года
    if not year.isdigit() or int(year) < 2023:
        await callback_query.answer("Некорректный год. Выберите текущий или будущий год.", show_alert=True)
        logger.error(f"Некорректный год: {year}")
        return
    logger.info(f"Выбран год начала: {year}")
    await state.update_data(start_year=year)  # Сохраняем год в FSM
    await callback_query.message.edit_text(
        "Выберите час начала мероприятия:",
        reply_markup=create_hour_keyboard("start")  # Переход к выбору часа
    )
    await state.set_state("select_start_hour")  # Устанавливаем состояние

# Обработчик выбора часа начала
@router.callback_query(lambda c: c.data.startswith("start_hour:"))
async def process_start_hour(callback_query: types.CallbackQuery, state: FSMContext):
    hour = callback_query.data.split(":")[1]
    # Проверка на валидность часа
    if not hour.isdigit() or int(hour) not in range(0, 24):
        await callback_query.answer("Некорректный час. Выберите в диапазоне от 0 до 23.", show_alert=True)
        logger.error(f"Некорректный час: {hour}")
        return
    logger.info(f"Выбран час начала: {hour}")
    await state.update_data(start_hour=hour)  # Сохраняем час в FSM
    await callback_query.message.edit_text(
        "Выберите минуты начала мероприятия:",
        reply_markup=create_minute_keyboard("start")  # Переход к выбору минут
    )
    await state.set_state("select_start_minute")  # Устанавливаем состояние

# Обработчик выбора минуты начала
@router.callback_query(lambda c: c.data.startswith("start_minute:"))
async def process_start_minute(callback_query: types.CallbackQuery, state: FSMContext):
    minute = callback_query.data.split(":")[1]
    # Проверка на валидность минут
    if not minute.isdigit() or int(minute) not in range(0, 60):
        await callback_query.answer("Некорректные минуты. Выберите в диапазоне от 0 до 59.", show_alert=True)
        logger.error(f"Некорректные минуты: {minute}")
        return
    logger.info(f"Выбраны минуты начала: {minute}")
    await state.update_data(start_minute=minute)  # Сохраняем минуты в FSM

    # Формирование сообщения для перехода к выбору окончания мероприятия
    await callback_query.message.edit_text(
        "Выберите час окончания мероприятия:",
        reply_markup=create_hour_keyboard("end")  # Переход к выбору часа окончания
    )
    await state.set_state("select_end_hour")  # Устанавливаем состояние
