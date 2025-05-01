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
        # Извлечение ID предпочтения
        preference_id = int(callback_query.data.split(":")[1])

        # Получение текущих данных FSM
        user_data = await state.get_data()
        preferences = user_data.get("preferences", [])

        # Если предпочтение не выбрано, добавляем его
        if not any(pref["id"] == preference_id for pref in preferences):
            preferences.append({"id": preference_id})
            await state.update_data(preferences=preferences)
            await callback_query.answer("✅ Предпочтение выбрано!", show_alert=False)
        else:
            await callback_query.answer("⚠️ Вы уже выбрали это предпочтение.", show_alert=True)

        logger.info(f"Обновленные предпочтения: {preferences}")
    except ValueError:
        logger.error("Ошибка обработки ID предпочтения.")
        await callback_query.answer("⚠️ Ошибка! Попробуйте снова.", show_alert=True)
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        await callback_query.answer("❌ Произошла ошибка. Попробуйте позже.", show_alert=True)
