from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from ..config import logger, DJANGO_API_BASE_URL

router = Router()

@router.callback_query(lambda c: c.data == "finalize_booking")
async def finalize_booking(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработчик для завершения бронирования и отправки данных на сервер.
    """
    try:
        # Получаем данные из FSM
        state_data = await state.get_data()

        # Проверяем, была ли заявка уже отправлена
        if state_data.get("booking_finalized"):
            await callback_query.answer("✅ Заявка на бронирование уже подтверждена.", show_alert=True)
            logger.info("Попытка повторного подтверждения бронирования.")
            return

        user_data = state_data
        logger.info(f"Данные пользователя перед отправкой: {user_data}")

        # Проверка обязательных данных
        required_keys = [
            "start_year", "start_month", "start_day", "start_hour", "start_minute",
            "end_hour", "end_minute", "event_end_date",
            "guests_count", "selected_hall", "preferences",
            "name", "phone", "call_time", "messenger", "promo_code"
        ]
        missing_keys = [key for key in required_keys if key not in user_data or not user_data[key]]

        if missing_keys:
            logger.error(f"Пропущенные обязательные данные: {missing_keys}")
            await callback_query.answer(
                f"❌ Проблема с данными. Не хватает: {', '.join(missing_keys)}.",
                show_alert=True
            )
            return

        # Проверка формата времени звонка (call_time)
        call_time = user_data.get("call_time", None)
        if ":" not in call_time:
            call_time = f"{call_time}:00:00"  # Форматируем время звонка

        # Формирование дат в формате ISO 8601
        event_start_date = (
            f"{user_data['start_year']}-"
            f"{int(user_data['start_month']):02}-"
            f"{int(user_data['start_day']):02}T"
            f"{int(user_data['start_hour']):02}:{int(user_data['start_minute']):02}:00Z"
        )
        from datetime import datetime
        event_end_date = datetime(
            year=int(user_data["start_year"]),
            month=int(user_data["start_month"]),
            day=int(user_data["start_day"]),
            hour=int(user_data["end_hour"]),
            minute=int(user_data["end_minute"])
        ).isoformat(timespec="seconds") + "Z"

        # Формирование JSON для отправки на сервер
        booking_data = {
            "event_start_date": event_start_date,
            "event_end_date": event_end_date,
            "space": user_data["selected_hall"]["id"],
            "preferences": [pref["id"] for pref in user_data.get("preferences", [])],
            "client_name": user_data["name"],
            "client_contact": user_data["phone"],
            "call_time": call_time,
            "guests_count": user_data["guests_count"],
            "messenger": user_data.get("messenger", "не указан"),
            "promo_code": user_data.get("promo_code", None)
        }

        logger.info(f"Данные для отправки на сервер: {booking_data}")

        # Отправка данных на сервер
        async with ClientSession() as session:
            async with session.post(f"{DJANGO_API_BASE_URL}create-booking/", json=booking_data) as response:
                if response.status == 201:
                    logger.info("Бронирование успешно создано на сервере.")
                    await callback_query.answer("🎉 Заявка принята! В ближайшее время мы Вам перезвоним!", show_alert=True)
                    await state.update_data(booking_finalized=True)  # Фиксируем успешное бронирование
                else:
                    error_text = await response.text()
                    logger.error(f"Ошибка от сервера: {response.status}. Текст ошибки: {error_text}")
                    await callback_query.answer(
                        f"⚠️ Ошибка сервера. Код ошибки: {response.status}. Подробнее: {error_text}",
                        show_alert=True
                    )
                    return

    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        await callback_query.answer("❌ Произошла ошибка. Попробуйте позже или обратитесь в поддержку.", show_alert=True)
