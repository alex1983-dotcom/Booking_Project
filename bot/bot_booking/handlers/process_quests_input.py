from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from ..config import logger, DJANGO_API_BASE_URL
from aiogram.filters import StateFilter
from ..keyboards import create_halls_keyboard

router = Router()

@router.message(StateFilter("enter_guests"))
async def process_guests_input(message: types.Message, state: FSMContext):
    """
    Обработчик ввода количества гостей и запроса доступных залов.
    """
    try:
        # Проверка на корректность ввода количества гостей
        guests_count = int(message.text.strip())
        if guests_count <= 0:
            raise ValueError("Количество гостей должно быть положительным числом.")
    except ValueError:
        await message.reply("⚠️ Пожалуйста, введите корректное количество гостей (положительное целое число).")
        return

    # Сохраняем количество гостей в FSM
    await state.update_data(guests_count=guests_count)
    user_data = await state.get_data()
    logger.info(f"Текущее состояние данных пользователя: {user_data}")

    # Формируем параметры времени для запроса
    start_datetime = f"{user_data['start_year']}-{int(user_data['start_month']):02}-{int(user_data['start_day']):02} {int(user_data['start_hour']):02}:{int(user_data['start_minute']):02}"
    end_datetime = f"{user_data['start_year']}-{int(user_data['start_month']):02}-{int(user_data['start_day']):02} {int(user_data['end_hour']):02}:{int(user_data['end_minute']):02}"

    # Отправляем запрос на сервер для проверки доступных залов
    async with ClientSession() as session:
        try:
            response = await session.get(
                f"{DJANGO_API_BASE_URL}check-availability/",
                params={
                    "start": start_datetime,
                    "end": end_datetime,
                    "guests": guests_count
                }
            )

            if response.status == 200:
                response_data = await response.json()
                halls = response_data.get("data", {}).get("spaces", [])
                logger.info(f"Найдены залы: {halls}")

                if halls:
                    await message.reply(
                        "🏢 Доступные залы найдены! Выберите один из них:",
                        reply_markup=create_halls_keyboard(halls)
                    )
                    await state.set_state("hall_selection")
                else:
                    logger.warning("Нет доступных залов для указанных параметров.")
                    await message.reply("⚠️ Нет доступных залов для указанного времени. Попробуйте изменить параметры бронирования.")
            else:
                response_text = await response.text()
                logger.error(f"Ошибка сервера: статус {response.status}. Ответ: {response_text}")
                await message.reply("⚠️ Произошла ошибка при проверке залов. Попробуйте позже.")

        except Exception as e:
            logger.error(f"Ошибка при отправке запроса: {str(e)}")
            await message.reply(f"❌ Ошибка соединения с сервером: {str(e)}")
