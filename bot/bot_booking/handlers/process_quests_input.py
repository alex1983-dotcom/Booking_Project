from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from ..config import logger, DJANGO_API_BASE_URL
from aiogram.filters import StateFilter
from ..keyboards import create_halls_keyboard

router = Router()

# ======================= Обработчик ввода количества гостей ====================
@router.message(StateFilter("enter_guests"))
async def process_guests_input(message: types.Message, state: FSMContext):
    """
    Обработчик ввода количества гостей, проверки параметров и запроса доступных залов.
    """
    try:
        # Проверяем ввод количества гостей
        guests_count = int(message.text.strip())
        if guests_count <= 0:
            raise ValueError("Количество гостей должно быть положительным числом.")
    except ValueError:
        await message.reply("⚠️ Пожалуйста, введите корректное количество гостей (положительное целое число).")
        return

    # Сохраняем количество гостей в состоянии
    await state.update_data(guests_count=guests_count)
    user_data = await state.get_data()

    try:
        # Формируем параметры времени
        start_hour = int(user_data.get("start_hour", 0))
        end_hour = int(user_data.get("end_hour", 0))
        start_minute = int(user_data.get("start_minute", 0))
        end_minute = int(user_data.get("end_minute", 0))

        # Проверяем корректность времени
        if not (0 <= start_hour <= 23 and 0 <= end_hour <= 23 and 0 <= start_minute <= 59 and 0 <= end_minute <= 59):
            await message.reply("⚠️ Ошибка: Часы должны быть в диапазоне 0-23, а минуты — в диапазоне 0-59. Пожалуйста, проверьте данные.")
            return

        # Формируем строки даты и времени
        start_datetime = f"{user_data['start_year']}-{user_data['start_month']:02}-{user_data['start_day']:02} {start_hour:02}:{start_minute:02}"
        end_datetime = f"{user_data['end_year']}-{user_data['end_month']:02}-{user_data['end_day']:02} {end_hour:02}:{end_minute:02}"
    except KeyError as e:
        await message.reply(f"⚠️ Ошибка формирования параметров времени: отсутствует {e}. Пожалуйста, начните процесс заново с /start.")
        return

    # Логируем параметры для отладки
    logger.info(f"Параметры запроса: start={start_datetime}, end={end_datetime}, guests={guests_count}")

    # Отправляем запрос к серверу
    async with ClientSession() as session:
        try:
            response = await session.get(f"{DJANGO_API_BASE_URL}check-availability/", params={
                "start": start_datetime,
                "end": end_datetime,
                "guests": guests_count
            })

            if response.status == 200:
                # Обрабатываем успешный ответ от сервера
                response_data = await response.json()
                halls = response_data.get("spaces", [])
                if halls:
                    await message.reply("🏢 Доступные залы найдены! Выберите один из них:", reply_markup=create_halls_keyboard(halls))
                    await state.set_state("hall_selection")
                else:
                    await message.reply("⚠️ Нет доступных залов для указанного времени. Попробуйте изменить параметры бронирования.")
            elif response.status == 400:
                await message.reply("⚠️ Некорректный запрос. Проверьте параметры и попробуйте снова.")
                logger.warning(f"400 Bad Request. Параметры: start={start_datetime}, end={end_datetime}, guests={guests_count}")
            else:
                await message.reply("⚠️ Произошла ошибка при проверке залов. Попробуйте позже.")
                logger.error(f"Ошибка сервера: статус {response.status}. Параметры: start={start_datetime}, end={end_datetime}, guests={guests_count}")
        except Exception as e:
            await message.reply(f"❌ Ошибка соединения с сервером: {str(e)}")
            logger.error(f"Ошибка при отправке запроса: {str(e)}")

