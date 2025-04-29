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
    Финальное сохранение контактных данных и отправка на сервер.
    """
    try:
        # Получаем данные из FSM
        user_data = await state.get_data()
        logger.info(f"Данные пользователя перед завершением: {user_data}")

        # Обработка отсутствующих значений
        promo_code = user_data.get("promo_code", "Не введён")
        messenger = user_data.get("messenger", "Не выбран")
        await state.update_data(promo_code=promo_code, messenger=messenger)

        # Проверка обязательных данных
        required_fields = ["name", "phone", "call_time"]
        missing_fields = [field for field in required_fields if not user_data.get(field)]

        if missing_fields:
            await callback_query.message.reply(
                f"⚠️ Отсутствуют данные: {', '.join(missing_fields)}. Проверьте ввод."
            )
            logger.warning(f"Пропущенные обязательные данные: {missing_fields}")
            return

        # Формирование итогового сообщения
        message_text = (
            f"✅ Ваши данные успешно сохранены:\n\n"
            f"Имя: {user_data['name']}\n"
            f"Телефон: {user_data['phone']}\n"
            f"Время звонка: {user_data['call_time']}\n"  # Изменено на call_time
            f"Мессенджер: {messenger}\n"
            f"Промокод: {promo_code}\n\n"
            "Выберите дальнейшее действие:"
        )
        logger.info("Финальное сообщение отправлено пользователю.")

        # Отправка сообщения пользователю
        await callback_query.message.edit_text(
            message_text,
            reply_markup=create_finish_keyboard()
        )

        logger.info("Ввод контактных данных завершён успешно.")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}")
        await callback_query.message.reply("❌ Произошла ошибка. Попробуйте позже.")
