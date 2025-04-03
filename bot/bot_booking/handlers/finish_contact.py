import aiohttp
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from ..keyboards import create_finish_keyboard
from ..config import logger

API_URL = "http://127.0.0.1:8000/api/booking/"

router = Router()

@router.callback_query(lambda c: c.data == "contact_input")
async def finish_contact(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает ввод контактных данных.
    """
    user_data = await state.get_data()

    # Проверка обязательных данных
    if not all(key in user_data for key in ["name", "phone", "email"]):
        await callback_query.message.reply("⚠️ Не все данные введены. Проверьте ввод.")
        return

    async with aiohttp.ClientSession() as session:
        payload = {
            "name": user_data.get("name"),
            "phone_number": user_data.get("phone"),
            "email": user_data.get("email"),
            "promo_code": user_data.get("promo_code", None),
            "messengers": int(user_data.get("messenger", 1))  # 1 = Viber по умолчанию
        }
        try:
            async with session.post(API_URL, json=payload) as response:
                if response.status == 201:
                    await callback_query.message.reply(
                        "✅ Контактные данные успешно сохранены! Выберите дальнейшее действие:",
                        reply_markup=create_finish_keyboard()
                    )
                else:
                    await callback_query.message.reply(
                        f"⚠️ Ошибка при сохранении данных: {await response.text()}."
                    )
        except Exception as e:
            logger.error(f"Ошибка соединения с API: {e}")
            await callback_query.message.reply("❌ Произошла ошибка связи с сервером. Попробуйте позже.")

    await state.clear()
