from aiohttp import ClientSession
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from ..keyboards import create_preferences_keyboard
from ..config import logger, DJANGO_API_BASE_URL

router = Router()

@router.callback_query(lambda c: c.data.startswith("hall:"))
async def process_hall_selection(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработчик выбора зала.
    """
    try:
        # Извлечение ID выбранного зала из callback_data
        hall_id = callback_query.data.split(":")[1]
        await state.update_data(selected_hall=hall_id)

        # Запрос к API для получения предпочтений
        async with ClientSession() as session:
            response = await session.get(f"{DJANGO_API_BASE_URL}get-preferences/")
            
            # Проверяем статус ответа
            if response.status == 200:
                response_data = await response.json()  # Преобразуем JSON-строку в объект Python
                
                # Извлечение предпочтений
                preferences = response_data.get("preferences", [])
                
                # Проверяем, что preferences — это список словарей
                if not isinstance(preferences, list):
                    raise ValueError("Данные preferences должны быть списком.")
                
                # Проверяем, что каждый элемент в списке — это словарь
                if not all(isinstance(pref, dict) for pref in preferences):
                    raise ValueError("Элементы preferences должны быть словарями.")
                
                # Генерация клавиатуры и вывод доступных предпочтений
                await callback_query.message.edit_text(
                    "Выберите дополнительные предпочтения:",
                    reply_markup=create_preferences_keyboard(preferences)
                )

                # Устанавливаем новое состояние
                await state.set_state("preferences_selection")
            else:
                await callback_query.message.reply(
                    "⚠️ Ошибка при получении данных о предпочтениях. Попробуйте позже."
                )
                logger.error(f"Ошибка API: статус {response.status}")
    except ValueError as ve:
        # Обработка ошибок связанных с типом данных
        await callback_query.message.reply(f"⚠️ Ошибка: {str(ve)}")
        logger.error(f"Ошибка данных: {str(ve)}")
    except KeyError as ke:
        # Обработка отсутствующих ключей
        await callback_query.message.reply(f"⚠️ Ошибка: отсутствует ключ {str(ke)}.")
        logger.error(f"Ошибка данных: отсутствует ключ {str(ke)}")
    except Exception as e:
        # Общая обработка ошибок
        await callback_query.message.reply(f"❌ Произошла ошибка: {str(e)}")
        logger.error(f"Неожиданная ошибка в process_hall_selection: {str(e)}")
