from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from ..config import logger

router = Router()

@router.callback_query(lambda c: c.data.startswith("preference:"))
async def process_preferences_selection(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработчик выбора предпочтений.
    """
    preference_id = callback_query.data.split(":")[1]
    user_data = await state.get_data()

    # Добавляем выбранное предпочтение в состояние
    preferences = user_data.get("preferences", [])
    if not any(pref["id"] == preference_id for pref in preferences):
        preferences.append({"id": preference_id, "name": f"{preference_id}"})  # Пример названия

    await state.update_data(preferences=preferences)

    # Отправляем временное уведомление, что предпочтение добавлено
    await callback_query.answer("✅ Предпочтение добавлено!", show_alert=False)

  
