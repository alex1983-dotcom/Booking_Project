from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from datetime import datetime
from ..config import logger, DJANGO_API_BASE_URL

router = Router()

@router.callback_query(lambda c: c.data == "finalize_booking")
async def finalize_booking(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработчик завершения бронирования и отправки данных на сервер.
    """
    try:
        state_data = await state.get_data()

        # Проверяем, была ли заявка уже отправлена
        if state_data.get("booking_finalized"):
            await callback_query.answer("✅ Заявка уже подтверждена.", show_alert=True)
            logger.info("Попытка повторного подтверждения бронирования.")
            return

        user_data = state_data
        logger.info(f"Данные перед обработкой: {user_data}")

        # --- Обработка messengers ---
        messenger_mapping = {
            "viber": 1,
            "telegram": 2,
            "whatsapp": 3
        }

        messenger_value = user_data.get("messenger")

        # Проверяем, является ли messenger строкой перед вызовом `.lower()`
        if isinstance(messenger_value, str):
            messenger_value = messenger_value.lower()

        user_data["messenger"] = messenger_mapping.get(messenger_value, 0)

        logger.info(f"Обработанный messenger: {user_data['messenger']}")

        # --- Обработка call_time ---
        call_time = user_data.get("call_time")

        # Если call_time отсутствует или некорректно передано, используем стандартный формат
        if not call_time or not isinstance(call_time, str) or ":" not in call_time:
            call_time = "10:00"

        logger.info(f"Обработанный call_time: {call_time}")

        # --- Формирование ISO 8601 дат ---
        event_start_date = datetime(
            int(user_data["start_year"]), int(user_data["start_month"]), int(user_data["start_day"]),
            int(user_data["start_hour"]), int(user_data["start_minute"])
        ).isoformat(timespec="seconds") + "Z"

        event_end_date = datetime(
            int(user_data["start_year"]), int(user_data["start_month"]), int(user_data["start_day"]),
            int(user_data["end_hour"]), int(user_data["end_minute"])
        ).isoformat(timespec="seconds") + "Z"

        # --- Формирование JSON для отправки на сервер ---
        booking_data = {
            "event_start_date": event_start_date,
            "event_end_date": event_end_date,
            "space": user_data["selected_hall"]["id"],
            "preferences": [pref["id"] for pref in user_data.get("preferences", [])],
            "client_name": user_data["name"],
            "client_contact": user_data["phone"],
            "call_time": call_time,
            "guests_count": user_data["guests_count"],
            "messenger": user_data["messenger"],
            "promo_code": user_data.get("promo_code", None)
        }

        logger.info(f"Данные перед отправкой: {booking_data}")

        # --- Отправка запроса на сервер ---
        async with ClientSession() as session:
            async with session.post(f"{DJANGO_API_BASE_URL}create-booking/", json=booking_data) as response:
                if response.status == 201:
                    await callback_query.answer("🎉 Заявка принята!", show_alert=True)
                    await state.update_data(booking_finalized=True)
                    logger.info("Бронирование успешно создано.")
                else:
                    error_text = await response.text()
                    logger.error(f"Ошибка сервера: {error_text}")
                    await callback_query.answer(f"⚠️ Ошибка: {error_text}", show_alert=True)

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        await callback_query.answer("❌ Ошибка обработки бронирования.", show_alert=True)
