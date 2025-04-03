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
    """
    Обработчик для завершения бронирования.
    """
    user_data = await state.get_data()

    async with ClientSession() as session:
        try:
            # Отправляем запрос для создания бронирования
            async with session.post(f"{DJANGO_API_BASE_URL}create-booking/", json=user_data) as response:
                if response.status == 201:
                    await callback_query.message.edit_text("🎉 Ваше бронирование успешно завершено!")
                    logger.info("Бронирование успешно завершено.")
                else:
                    logger.error(f"Ошибка при создании бронирования. Статус: {response.status}")
                    await callback_query.message.edit_text(
                        "⚠️ Произошла ошибка при создании бронирования. Попробуйте ещё раз."
                    )
        except Exception as e:
            logger.error(f"Ошибка связи с сервером: {e}")
            await callback_query.message.edit_text("❌ Не удалось завершить бронирование. Попробуйте позже.")

    # Очищаем состояние
    await state.clear()
