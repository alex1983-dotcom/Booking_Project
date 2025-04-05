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
        user_data = await state.get_data()

        # Проверка обязательных данных
        required_keys = [
            "start_year", "start_month", "start_day", "start_hour", "start_minute",
            "end_year", "end_month", "end_day", "end_hour", "end_minute",
            "selected_hall", "preferences", "name", "phone", "guests_count", "email", "messenger"
        ]
        missing_keys = [key for key in required_keys if key not in user_data or not user_data[key]]
        if missing_keys:
            logger.error(f"Пропущенные обязательные данные: {missing_keys}")
            await callback_query.answer(
                f"❌ Проблема с данными. Не хватает: {', '.join(missing_keys)}.",
                show_alert=True
            )
            return

        # Формирование дат в формате ISO 8601
        event_start_date = (
            f"{user_data['start_year']}-"
            f"{int(user_data['start_month']):02}-"
            f"{int(user_data['start_day']):02}T"
            f"{int(user_data['start_hour']):02}:"
            f"{int(user_data['start_minute']):02}:00Z"
        )
        event_end_date = (
            f"{user_data['end_year']}-"
            f"{int(user_data['end_month']):02}-"
            f"{int(user_data['end_day']):02}T"
            f"{int(user_data['end_hour']):02}:"
            f"{int(user_data['end_minute']):02}:00Z"
        )

        # Формирование данных для сервера
        booking_data = {
            "event_start_date": event_start_date,
            "event_end_date": event_end_date,
            "space": user_data["selected_hall"]["id"],
            "preferences": [pref["id"] for pref in user_data.get("preferences", [])],
            "client_name": user_data["name"],
            "client_contact": user_data["phone"],
            "guests_count": user_data["guests_count"],
            "email": user_data["email"],
            "messenger": user_data.get("messenger", "не указан")
        }

        logger.info(f"Отправка данных на сервер: {booking_data}")

        # Отправка данных на сервер
        async with ClientSession() as session:
            async with session.post(f"{DJANGO_API_BASE_URL}create-booking/", json=booking_data) as response:
                if response.status == 201:
                    logger.info("Бронирование успешно создано на сервере.")
                    await callback_query.answer("🎉 Бронирование успешно завершено!", show_alert=True)
                else:
                    error_text = await response.text()
                    logger.error(f"Ошибка от сервера: {response.status}. Текст ошибки: {error_text}")
                    await callback_query.answer(
                        f"⚠️ Ошибка сервера. Код ошибки: {response.status}. Подробности: {error_text}",
                        show_alert=True
                    )
                    return

    except Exception as e:
        logger.error(f"Неожиданная ошибка при обработке бронирования: {e}")
        await callback_query.answer("❌ Произошла ошибка. Попробуйте позже или обратитесь в поддержку.", show_alert=True)
