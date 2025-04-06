from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from datetime import datetime
from ..keyboards import create_minute_keyboard
from ..config import logger

router = Router()

# Обработчик выбора часа окончания
@router.callback_query(lambda c: c.data.startswith("end_hour:"))
async def process_end_hour(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработчик выбора часа окончания мероприятия.
    """
    hour = callback_query.data.split(":")[1]
    # Проверка на валидность часа
    if not hour.isdigit() or int(hour) not in range(0, 24):
        await callback_query.answer("Некорректный час. Выберите в диапазоне от 0 до 23.", show_alert=True)
        logger.error(f"Некорректный час: {hour}")
        return
    logger.info(f"Выбран час окончания: {hour}")

    # Сохраняем час окончания в FSM
    await state.update_data(end_hour=hour)

    # Переход к выбору минут окончания
    await callback_query.message.edit_text(
        "Выберите минуты окончания мероприятия:",
        reply_markup=create_minute_keyboard("end")
    )
    await state.set_state("select_end_minute")  # Обновление состояния FSM

# Обработчик выбора минут окончания
@router.callback_query(lambda c: c.data.startswith("end_minute:"))
async def process_end_minute(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработчик выбора минут окончания мероприятия.
    """
    minute = callback_query.data.split(":")[1]
    # Проверка на валидность минут
    if not minute.isdigit() or int(minute) not in range(0, 60):
        await callback_query.answer("Некорректные минуты. Выберите в диапазоне от 0 до 59.", show_alert=True)
        logger.error(f"Некорректные минуты: {minute}")
        return
    logger.info(f"Выбраны минуты окончания: {minute}")

    # Сохраняем минуты окончания в FSM
    await state.update_data(end_minute=minute)

    # Получаем данные из FSM для проверки
    user_data = await state.get_data()
    logger.info(f"Текущее состояние FSM: {user_data}")

    # Проверка обязательных данных перед формированием времени окончания
    required_keys = ["start_year", "start_month", "start_day", "end_hour", "end_minute"]
    missing_keys = [key for key in required_keys if key not in user_data or not user_data[key]]

    if missing_keys:
        logger.error(f"Пропущенные обязательные данные: {missing_keys}")
        await callback_query.answer(
            f"❌ Пропущенные данные: {', '.join(missing_keys)}. Пожалуйста, начните процесс заново.",
            show_alert=True
        )
        return

    try:
        # Формируем дату и время окончания
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

    # Переход к следующему этапу: ввод количества гостей
    await callback_query.message.edit_text("Введите количество гостей:")
    await state.set_state("enter_guests")  # Обновление состояния FSM
