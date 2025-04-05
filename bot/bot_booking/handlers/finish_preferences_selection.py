from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from ..keyboards import create_contact_input_keyboard
from ..config import logger

router = Router()

@router.callback_query(lambda c: c.data == "finish_selection")
async def finish_preferences_selection(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Завершение выбора предпочтений и переход к вводу контактных данных.
    """
    # Получаем данные из состояния
    user_data = await state.get_data()
    preferences = user_data.get("preferences", [])

    # Формируем итоговое сообщение о выбранных предпочтениях
    if preferences:
        preferences_names = "\n".join([pref["name"] for pref in preferences])
        message = f"✅ Вы выбрали следующие предпочтения:\n{preferences_names}"
    else:
        message = "❌ Вы не выбрали никаких предпочтений."

    # Обновляем сообщение с итогами выбора
    await callback_query.message.edit_text(message)

    # Переход к следующему этапу с кнопкой (без текста)
    await callback_query.message.edit_reply_markup(reply_markup=create_contact_input_keyboard())
    
    # Устанавливаем состояние для ввода контактных данных
    await state.set_state("start_contact_input")

    # Логирование для отладки
    logger.info("Переход к состоянию 'start_contact_input'.")
