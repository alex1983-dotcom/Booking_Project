from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from ..config import logger, DJANGO_API_BASE_URL
from ..keyboards import create_preferences_keyboard

router = Router()

async def fetch_preferences_from_db():
    """
    Получение списка опций из базы данных через API.
    """
    async with ClientSession() as session:
        try:
            async with session.get(f"{DJANGO_API_BASE_URL}get-preferences/") as response:
                logger.info(f"HTTP статус ответа: {response.status}")
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Полученные предпочтения от API: {data}")
                    return data.get("data", {}).get("preferences", [])
                else:
                    logger.error(f"Ошибка при получении предпочтений: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Ошибка при запросе предпочтений: {e}")
            return []

@router.callback_query(lambda c: c.data.startswith("hall:"))
async def process_single_hall_selection(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработчик выбора единственного зала с переходом к предпочтениям.
    """
    try:
        hall_id = int(callback_query.data.split(":")[1])

        # Сохраняем выбранный зал в FSM
        selected_hall = {"id": hall_id, "name": f"Зал {hall_id}"}
        await state.update_data(selected_hall=selected_hall)
        logger.info(f"Выбранный зал: {selected_hall}")

        # Проверяем данные в FSM
        user_data = await state.get_data()
        logger.info(f"Текущее состояние данных FSM после выбора зала: {user_data}")

        # Отправляем сообщение пользователю
        await callback_query.message.reply(f"Вы выбрали зал: {selected_hall['name']}")

        # Получаем список предпочтений через API
        preferences = await fetch_preferences_from_db()

        if preferences:
            # Генерация клавиатуры с предпочтениями
            keyboard = create_preferences_keyboard(preferences)
            await callback_query.message.reply("Теперь выберите предпочтения:", reply_markup=keyboard)
            await state.set_state("preference")  # Устанавливаем состояние выбора предпочтений
        else:
            logger.warning("Предпочтения недоступны.")
            await callback_query.message.reply("❌ Предпочтения недоступны. Попробуйте позже.")
    except ValueError:
        logger.error("Некорректный ID зала в callback_data.")
        await callback_query.answer("Некорректные данные. Пожалуйста, попробуйте снова.", show_alert=True)
    except Exception as e:
        logger.error(f"Ошибка при обработке выбора зала: {str(e)}")
        await callback_query.answer("Произошла ошибка. Попробуйте позже.", show_alert=True)
