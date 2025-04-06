from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from datetime import datetime
from ..config import logger, DJANGO_API_BASE_URL
from aiogram.filters import StateFilter
from ..keyboards import create_halls_keyboard

router = Router()

@router.message(StateFilter("enter_guests"))
async def process_guests_input(message: types.Message, state: FSMContext):
    """
    Обработчик ввода количества гостей, проверки параметров и запроса доступных залов.
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

    try:
        # Проверяем наличие всех данных в FSM
        required_keys = ["start_year", "start_month", "start_day", "start_hour", "start_minute", "end_hour", "end_minute"]
        missing_keys = [key for key in required_keys if key not in user_data]

        if missing_keys:
            logger.error(f"Пропущенные ключи: {missing_keys}")
            await message.reply(f"⚠️ Ошибка: отсутствуют ключи {', '.join(missing_keys)}. Пожалуйста, начните заново с команды /start.")
            return

        # Формируем параметры времени для запроса
        start_datetime = f"{user_data['start_year']}-{int(user_data['start_month']):02}-{int(user_data['start_day']):02} {int(user_data['start_hour']):02}:{int(user_data['start_minute']):02}"
        end_datetime = f"{user_data['start_year']}-{int(user_data['start_month']):02}-{int(user_data['start_day']):02} {int(user_data['end_hour']):02}:{int(user_data['end_minute']):02}"

        if end_datetime <= start_datetime:
            logger.error("Время окончания меньше или равно времени начала.")
            await message.reply("⚠️ Время окончания должно быть позже времени начала.")
            return

        logger.info(f"Параметры запроса: start={start_datetime}, end={end_datetime}, guests={guests_count}")

    except KeyError as e:
        logger.error(f"Ошибка: отсутствует ключ {e} в состоянии данных.")
        await message.reply(f"⚠️ Ошибка: отсутствует ключ {e}. Пожалуйста, начните процесс заново с команды /start.")
        return
    except Exception as e:
        logger.error(f"Ошибка при обработке данных: {e}")
        await message.reply(f"⚠️ Произошла ошибка: {str(e)}")
        return

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
            elif response.status == 400:
                response_text = await response.text()
                logger.warning(f"Некорректный запрос: статус 400. Ответ сервера: {response_text}")
                await message.reply(f"⚠️ Некорректный запрос. Сообщение от сервера: {response_text}")
            else:
                logger.error(f"Ошибка сервера: статус {response.status}. Параметры: start={start_datetime}, end={end_datetime}, guests={guests_count}")
                await message.reply("⚠️ Произошла ошибка при проверке залов. Попробуйте позже.")

        except Exception as e:
            logger.error(f"Ошибка при отправке запроса: {str(e)}")
            await message.reply(f"❌ Ошибка соединения с сервером: {str(e)}")
