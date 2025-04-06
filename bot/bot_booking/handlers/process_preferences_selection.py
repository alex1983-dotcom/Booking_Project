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
        # Извлечение ID выбранного предпочтения из callback_data
        preference_id = int(callback_query.data.split(":")[1])

        # Получение текущего состояния данных FSM
        user_data = await state.get_data()
        logger.info(f"Текущее состояние данных FSM перед выбором предпочтений: {user_data}")

        # Получение уже сохранённых предпочтений из FSM
        preferences = user_data.get("preferences", [])

        # Проверяем, добавлено ли уже выбранное предпочтение
        if not any(pref["id"] == preference_id for pref in preferences):
            preferences.append({"id": preference_id, "name": f"Предпочтение {preference_id}"})
            await state.update_data(preferences=preferences)  # Сохранение обновлённых предпочтений
            await callback_query.answer(f"✅ Предпочтение добавлено!", show_alert=False)
        else:
            await callback_query.answer(f"⚠️ Предпочтение уже выбрано!", show_alert=True)

        # Логирование текущих предпочтений после обновления
        logger.info(f"Текущие предпочтения после обновления: {preferences}")
    except ValueError:
        # Обработка некорректного preference_id
        logger.error("Некорректный ID предпочтения в callback_data.")
        await callback_query.answer("⚠️ Некорректный ID предпочтения. Попробуйте снова.", show_alert=True)
    except Exception as e:
        # Обработка общих ошибок
        logger.error(f"Ошибка при обработке выбора предпочтений: {str(e)}")
        await callback_query.answer("❌ Произошла ошибка. Попробуйте позже.", show_alert=True)
