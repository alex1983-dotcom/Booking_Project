from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from datetime import datetime
from ..keyboards import create_minute_keyboard
from ..config import logger

router = Router()

# Обработчик выбора часа окончания
@router.callback_query(lambda c: c.data.startswith("end_hour:"))
async def process_end_hour(callback_query: types.CallbackQuery, state: FSMContext):
    hour = callback_query.data.split(":")[1]
    if not hour.isdigit() or int(hour) not in range(0, 24):
        await callback_query.answer("Некорректный час. Выберите в диапазоне от 0 до 23.", show_alert=True)
        logger.error(f"Некорректный час: {hour}")
        return
    logger.info(f"Выбран час окончания: {hour}")
    await state.update_data(end_hour=hour)
    await callback_query.message.edit_text(
        "Выберите минуты окончания мероприятия:",
        reply_markup=create_minute_keyboard("end")
    )
    await state.set_state("select_end_minute")


# Обработчик выбора минут окончания
@router.callback_query(lambda c: c.data.startswith("end_minute:"))
async def process_end_minute(callback_query: types.CallbackQuery, state: FSMContext):
    minute = callback_query.data.split(":")[1]
    if not minute.isdigit() or int(minute) not in range(0, 60):
        await callback_query.answer("Некорректные минуты. Выберите в диапазоне от 0 до 59.", show_alert=True)
        logger.error(f"Некорректные минуты: {minute}")
        return
    logger.info(f"Выбраны минуты окончания: {minute}")
    await state.update_data(end_minute=minute)

    user_data = await state.get_data()
    logger.info(f"Текущее состояние FSM: {user_data}")

    try:
        # Формируем дату окончания мероприятия
        event_end_date = datetime(
            year=int(user_data["start_year"]),
            month=int(user_data["start_month"]),
            day=int(user_data["start_day"]),
            hour=int(user_data["end_hour"]),
            minute=int(user_data["end_minute"])
        )
        await state.update_data(event_end_date=event_end_date.isoformat())
        logger.info(f"Сформированное время окончания: {event_end_date}")
    except ValueError as e:
        logger.error(f"Ошибка при формировании времени окончания: {e}")
        await callback_query.answer("Ошибка при формировании времени. Проверьте данные.", show_alert=True)
        return

    await callback_query.message.edit_text("Введите количество гостей:")
    await state.set_state("enter_guests")
