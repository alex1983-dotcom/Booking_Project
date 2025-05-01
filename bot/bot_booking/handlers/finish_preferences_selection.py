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
    # Просто уведомляем пользователя, без списка предпочтений
    await callback_query.answer("✅ Ваши предпочтения выбраны!", show_alert=True)

    # Переход к следующему этапу
    await callback_query.message.edit_reply_markup(reply_markup=create_contact_input_keyboard())

    # Устанавливаем состояние для ввода контактных данных
    await state.set_state("start_contact_input")

    logger.info("Переход к 'start_contact_input'.")
