from aiogram import Router, types
from ..keyboards import create_preferences_keyboard
from ..config import logger
from aiogram.fsm.context import FSMContext

router = Router()

@router.callback_query(lambda c: c.data.startswith("preference:"))
async def process_preferences_selection(callback_query: types.CallbackQuery, state: FSMContext):
    # Извлекаем ID предпочтения из callback_data
    preference_id = callback_query.data.split(":")[1]
    user_data = await state.get_data()

    # Добавляем предпочтение в список
    preferences = user_data.get("preferences", [])
    
    # Проверяем, существует ли такое предпочтение уже
    if not any(pref['id'] == preference_id for pref in preferences):
        preferences.append({"id": preference_id, "name": f"Предпочтение {preference_id}"})  # Пример имени

    await state.update_data(preferences=preferences)

    # Отправляем сообщение о добавлении предпочтения
    await callback_query.answer("Предпочтение добавлено!")

    # Редактируем сообщение, передавая обновлённый список предпочтений
    await callback_query.message.edit_text(
        "Выберите ещё одно предпочтение или завершите выбор.",
        reply_markup=create_preferences_keyboard(preferences)  # Передаём список словарей
    )
