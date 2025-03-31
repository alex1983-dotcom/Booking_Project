from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from aiogram.filters import Command, StateFilter
from .keyboards import (
    create_calendar,
    create_month_keyboard,
    create_year_keyboard,
    create_hour_keyboard,
    create_minute_keyboard,
    create_halls_keyboard,
    create_preferences_keyboard,
    create_feedback_keyboard
)
from .config import logger, DJANGO_API_BASE_URL

# Создаем маршрутизатор
router = Router()

# === Обработчики ===

@router.message(Command(commands=['start']))
async def start_booking(message: types.Message, state: FSMContext):
    """
    Запуск процесса бронирования.
    """
    logger.info("Команда /start получена.")

    greeting = (
        "👋 Привет, я бот Innodom! 🤖\n\n"
        "Я помогу вам забронировать зал для вашего мероприятия.\n"
        "Вот что я умею:\n"
        "- 📅 Выбрать дату и время.\n"
        "- 🏢 Найти доступный зал.\n"
        "- ✅ Завершить бронирование.\n\n"
        "Давайте начнем!"
    )

    await message.reply(greeting)

    # Инструкция для выбора даты начала
    await message.reply("Выберите день начала мероприятия: 🗓️", reply_markup=create_calendar("start"))
    await state.set_state("select_start_day")


# Обработчики выбора даты начала мероприятия
@router.callback_query(lambda c: c.data.startswith("start_day:"))
async def process_start_day(callback_query: types.CallbackQuery, state: FSMContext):
    day = callback_query.data.split(":")[1]
    logger.info(f"Выбран день начала: {day}")
    await state.update_data(start_day=day)
    await callback_query.message.edit_text("Выберите месяц начала мероприятия: 🗓️", reply_markup=create_month_keyboard("start"))
    await state.set_state("select_start_month")


@router.callback_query(lambda c: c.data.startswith("start_month:"))
async def process_start_month(callback_query: types.CallbackQuery, state: FSMContext):
    month = callback_query.data.split(":")[1]
    logger.info(f"Выбран месяц начала: {month}")
    await state.update_data(start_month=month)
    await callback_query.message.edit_text("Выберите год начала мероприятия: 🗓️", reply_markup=create_year_keyboard("start"))
    await state.set_state("select_start_year")


@router.callback_query(lambda c: c.data.startswith("start_year:"))
async def process_start_year(callback_query: types.CallbackQuery, state: FSMContext):
    year = callback_query.data.split(":")[1]
    logger.info(f"Выбран год начала: {year}")
    await state.update_data(start_year=year)
    await callback_query.message.edit_text("Выберите час начала мероприятия:", reply_markup=create_hour_keyboard("start"))
    await state.set_state("select_start_hour")


@router.callback_query(lambda c: c.data.startswith("start_hour:"))
async def process_start_hour(callback_query: types.CallbackQuery, state: FSMContext):
    hour = callback_query.data.split(":")[1]
    logger.info(f"Выбран час начала: {hour}")
    await state.update_data(start_hour=hour)
    await callback_query.message.edit_text("Выберите минуты начала мероприятия:", reply_markup=create_minute_keyboard("start"))
    await state.set_state("select_start_minute")


@router.callback_query(lambda c: c.data.startswith("start_minute:"))
async def process_start_minute(callback_query: types.CallbackQuery, state: FSMContext):
    minute = callback_query.data.split(":")[1]
    logger.info(f"Выбраны минуты начала: {minute}")
    await state.update_data(start_minute=minute)
    await callback_query.message.edit_text("Выберите день окончания мероприятия:", reply_markup=create_calendar("end"))
    await state.set_state("select_end_day")


# Обработчики выбора даты окончания
@router.callback_query(lambda c: c.data.startswith("end_day:"))
async def process_end_day(callback_query: types.CallbackQuery, state: FSMContext):
    day = callback_query.data.split(":")[1]
    logger.info(f"Выбран день окончания: {day}")
    await state.update_data(end_day=day)
    await callback_query.message.edit_text("Выберите месяц окончания мероприятия:", reply_markup=create_month_keyboard("end"))
    await state.set_state("select_end_month")


@router.callback_query(lambda c: c.data.startswith("end_month:"))
async def process_end_month(callback_query: types.CallbackQuery, state: FSMContext):
    month = callback_query.data.split(":")[1]
    logger.info(f"Выбран месяц окончания: {month}")
    await state.update_data(end_month=month)
    await callback_query.message.edit_text("Выберите год окончания мероприятия:", reply_markup=create_year_keyboard("end"))
    await state.set_state("select_end_year")


@router.callback_query(lambda c: c.data.startswith("end_year:"))
async def process_end_year(callback_query: types.CallbackQuery, state: FSMContext):
    year = callback_query.data.split(":")[1]
    logger.info(f"Выбран год окончания: {year}")
    await state.update_data(end_year=year)
    await callback_query.message.edit_text("Выберите час окончания мероприятия:", reply_markup=create_hour_keyboard("end"))
    await state.set_state("select_end_hour")


@router.callback_query(lambda c: c.data.startswith("end_hour:"))
async def process_end_hour(callback_query: types.CallbackQuery, state: FSMContext):
    hour = callback_query.data.split(":")[1]
    logger.info(f"Выбран час окончания: {hour}")
    await state.update_data(end_hour=hour)
    await callback_query.message.edit_text("Выберите минуты окончания мероприятия:", reply_markup=create_minute_keyboard("end"))
    await state.set_state("select_end_minute")


@router.callback_query(lambda c: c.data.startswith("end_minute:"))
async def process_end_minute(callback_query: types.CallbackQuery, state: FSMContext):
    minute = callback_query.data.split(":")[1]
    logger.info(f"Выбраны минуты окончания: {minute}")
    await state.update_data(end_minute=minute)
    await callback_query.message.edit_text("Введите количество гостей:")
    await state.set_state("enter_guests")



# =======================Обработчик ввода количества гостей====================
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

#=========================== Обработчик выбора зала==========================
@router.callback_query(lambda c: c.data.startswith("hall:"))
async def process_hall_selection(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Обработчик выбора зала.
    """
    try:
        # Извлечение ID выбранного зала из callback_data
        hall_id = callback_query.data.split(":")[1]
        await state.update_data(selected_hall=hall_id)

        # Получаем данные о предпочтениях (могут быть из базы данных или заранее определены)
        preferences = ["Wi-Fi", "Проектор", "Микрофоны", "Кофе-брейк"]  # Пример списка предпочтений

        # Проверка типа данных предпочтений
        if not isinstance(preferences, list):
            raise ValueError("Предпочтения должны быть списком.")

        # Генерация клавиатуры и вывод доступных предпочтений
        await callback_query.message.edit_text(
            "Выберите дополнительные предпочтения:",
            reply_markup=create_preferences_keyboard(preferences)
        )

        # Устанавливаем новое состояние
        await state.set_state("preferences_selection")

    except ValueError as ve:
        # Обработка ошибок связанных с типами данных
        await callback_query.message.reply(f"⚠️ Ошибка: {str(ve)}. Проверьте данные.")
        logger.error(f"Ошибка данных: {str(ve)}")
    except IndexError:
        # Обработка ошибки при парсинге callback_data
        await callback_query.message.reply("⚠️ Ошибка: некорректный формат callback_data.")
        logger.error("Некорректный формат callback_data. Ожидается формат 'hall:<id>'.")
    except Exception as e:
        # Общая обработка ошибок
        await callback_query.message.reply(f"❌ Произошла ошибка: {str(e)}")
        logger.error(f"Неожиданная ошибка в process_hall_selection: {str(e)}")



#======================== Обработчик выбора предпочтений=======================
@router.callback_query(lambda c: c.data.startswith("preference:"))
async def process_preferences_selection(callback_query: types.CallbackQuery, state: FSMContext):
    preference_id = callback_query.data.split(":")[1]
    user_data = await state.get_data()

    # Добавляем предпочтение в список
    preferences = user_data.get("preferences", [])
    preferences.append(preference_id)
    await state.update_data(preferences=preferences)

    await callback_query.answer("Предпочтение добавлено!")
    await callback_query.message.edit_text("Выберите ещё одно предпочтение или завершите выбор.", reply_markup=create_preferences_keyboard())


# Обработчик завершения бронирования
@router.message(StateFilter("preferences_selection"))
async def finalize_booking(message: types.Message, state: FSMContext):
    """
    Сбор всех данных и завершение бронирования.
    """
    user_data = await state.get_data()

    async with ClientSession() as session:
        try:
            # Формируем запрос на создание бронирования
            response = await session.post(f"{DJANGO_API_BASE_URL}create-booking/", json=user_data)
            
            if response.status == 201:
                # Успешное создание бронирования
                await message.reply("🎉 Ваше бронирование успешно создано!")
                logger.info("Бронирование успешно завершено.")
            else:
                # Ошибка при создании бронирования
                logger.error(f"Ошибка при создании бронирования: статус {response.status}")
                await message.reply("⚠️ Произошла ошибка при создании бронирования. Попробуйте ещё раз.")

        except Exception as e:
            # Общий обработчик ошибок
            logger.error(f"Не удалось завершить бронирование: {e}")
            await message.reply("⚠️ Произошла внутренняя ошибка. Пожалуйста, попробуйте позже.")

    # Очистка состояния
    await state.clear()
