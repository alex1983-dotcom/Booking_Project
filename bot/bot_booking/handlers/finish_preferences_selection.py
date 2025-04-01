from aiogram import Router, types
from ..config import logger
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(lambda c: c.data == "finish_selection")
async def finish_preferences_selection(callback_query: types.CallbackQuery, state: FSMContext):
    # Получаем данные из состояния
    user_data = await state.get_data()
    preferences = user_data.get("preferences", [])

    # Проверяем, является ли элемент словарём
    if all(isinstance(pref, dict) for pref in preferences):
        preferences_names = "\n".join([pref['name'] for pref in preferences])
    else:
        preferences_names = "\n".join(preferences)  # Если это список строк

    # Формируем итоговое сообщение
    message = f"Вы выбрали следующие предпочтения:\n{preferences_names}" if preferences else "Вы не выбрали предпочтений."

    # Отправляем итоговое сообщение
    await callback_query.message.edit_text(message)

    # Сбрасываем состояние или переводим пользователя в другой этап
    await state.clear()
