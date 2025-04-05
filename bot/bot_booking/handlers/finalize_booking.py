from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from ..config import logger, DJANGO_API_BASE_URL
from ..keyboards import (
    create_finish_keyboard,
    create_contact_input_keyboard,
    create_promo_code_keyboard,
    create_finish_contact_keyboard
)

router = Router()

@router.callback_query(lambda c: c.data == "finalize_booking")
async def finalize_booking(callback_query: types.CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    # Формируем конечную дату
    try:
        event_end_date = f"{user_data['end_year']}-{user_data['end_month']:02}-{user_data['end_day']:02}T{user_data['end_hour']:02}:{user_data['end_minute']:02}:00Z"
    except KeyError as e:
        await callback_query.answer(f"❌ Проблема с данными: {e}. Пожалуйста, убедитесь, что все данные введены.", show_alert=True)
        return

    # Формируем данные для запроса
    data = {
        "event_start_date": f"{user_data['start_year']}-{user_data['start_month']:02}-{user_data['start_day']:02}T{user_data['start_hour']:02}:{user_data['start_minute']:02}:00Z",
        "event_end_date": event_end_date,
        "space": int(user_data['selected_hall']),
        "preferences": [pref["id"] for pref in user_data.get("preferences", [])],
        "client_name": user_data['name'],
        "client_contact": user_data['phone'],
        "guests_count": user_data.get("guests_count")  # Обязательно проверяем, что поле заполнено
    }

    async with ClientSession() as session:
        async with session.post(f"{DJANGO_API_BASE_URL}create-booking/", json=data) as response:
            if response.status == 201:
                await callback_query.message.edit_text("🎉 Ваше бронирование успешно завершено!")
            else:
                error_text = await response.text()
                await callback_query.message.edit_text(
                    f"⚠️ Ошибка при создании бронирования: {response.status}. Ответ: {error_text}"
                )
