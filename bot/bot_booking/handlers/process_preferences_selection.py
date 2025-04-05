from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from ..config import logger

router = Router()

@router.callback_query(lambda c: c.data.startswith("preference:"))
async def process_preferences_selection(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработчик выбора предпочтений.
    """
    try:
        preference_id = int(callback_query.data.split(":")[1])
        user_data = await state.get_data()
        preferences = user_data.get("preferences", [])

        # Проверяем, есть ли выбранное предпочтение в списке
        if not any(pref["id"] == preference_id for pref in preferences):
            preferences.append({"id": preference_id, "name": f"Предпочтение {preference_id}"})
            await state.update_data(preferences=preferences)
            await callback_query.answer(f"✅ Предпочтение добавлено!", show_alert=False)
        else:
            await callback_query.answer(f"⚠️ Предпочтение уже выбрано!", show_alert=True)

        logger.info(f"Текущие предпочтения: {preferences}")
    except Exception as e:
        logger.error(f"Ошибка при обработке выбора предпочтений: {str(e)}")
        await callback_query.answer("❌ Произошла ошибка. Попробуйте позже.", show_alert=True)
