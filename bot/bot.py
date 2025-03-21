import logging
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from aiogram import types


# Настройки бота и API
API_TOKEN = '7858593332:AAGhwrIZJsh3ZkhkfgLZ39Sh1GEG2RhpW80'
DJANGO_API_BASE_URL = "http://127.0.0.1:8000/booking/api/"
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())


# ================= FSM для процесса бронирования =================
class BookingState(StatesGroup):
    waiting_for_space = State()
    waiting_for_name = State()
    waiting_for_contact = State()
    waiting_for_date = State()
    waiting_for_end_date = State()


# ================= Команда /start =================
@dp.message(Command("start"))
async def start_command(message: Message):
    text = (
        "Привет! Я бот для бронирования залов, оборудования и парковок.\n\n"
        "Доступные команды:\n"
        "/spaces - список залов\n"
        "/equipments - список оборудования\n"
        "/parking - список парковок\n"
        "/book - создать бронирование"
    )
    await message.answer(text)


# ================= Команда /spaces =================
@dp.message(Command("spaces"))
async def list_spaces(message: Message):
    async with aiohttp.ClientSession() as session:
        try:
            # Запрашиваем список залов
            async with session.get(DJANGO_API_BASE_URL + "spaces/") as response_spaces:
                if response_spaces.status == 200:
                    spaces = await response_spaces.json()

                    # Формируем клавиатуру с кнопками для каждого зала
                    keyboard = InlineKeyboardMarkup(
                        inline_keyboard=[
                            [
                                InlineKeyboardButton(
                                    text=space["name"],
                                    callback_data=f"view_space_{space['id']}"
                                )
                            ]
                            for space in spaces
                        ]
                    )

                    # Отправляем сообщение с клавиатурой
                    await message.answer(
                        "Выберите зал, чтобы просмотреть подробную информацию:",
                        reply_markup=keyboard
                    )
                else:
                    await message.answer("Ошибка при получении списка залов.")
        except Exception as e:
            logging.error(f"Ошибка при загрузке данных о залах: {e}")
            await message.answer("Произошла ошибка при загрузке списка залов.")


@dp.callback_query(lambda c: c.data.startswith("view_space_"))
async def view_space_details(callback_query: types.CallbackQuery):
    space_id = int(callback_query.data.split("_")[-1])  # Получаем ID зала
    async with aiohttp.ClientSession() as session:
        try:
            # Запрашиваем данные о выбранном зале
            async with session.get(DJANGO_API_BASE_URL + f"spaces/{space_id}/") as response_space:
                if response_space.status == 200:
                    space = await response_space.json()
                else:
                    await callback_query.message.answer("Ошибка при загрузке данных о зале.")
                    return

            # Получаем данные о бронированиях для этого зала
            async with session.get(DJANGO_API_BASE_URL + "bookings/") as response_bookings:
                if response_bookings.status == 200:
                    bookings = await response_bookings.json()
                else:
                    bookings = []

            # Фильтруем бронирования по ID зала
            bookings_for_space = [
                booking for booking in bookings if int(booking["space"]) == space_id
            ]

            # Формируем ответ с данными о зале и бронированиях
            reply = (
                f"Информация о зале:\n"
                f"Название: {space['name']}\n"
                f"Площадь: {space['area']} м²\n"
                f"Вместимость: {space['capacity']}\n"
                f"Цена за час: {space['price']} BYN\n"
                f"Этаж: {space.get('floor', 'Не указан')}\n"
                f"Описание: {space.get('description', 'Нет описания')}\n\n"
                f"Бронирования:\n"
            )

            if bookings_for_space:
                for booking in bookings_for_space:
                    reply += f"- Начало: {booking['date']}, Конец: {booking['end_date']}\n"
            else:
                reply += "Нет бронирований для этого зала.\n"

            # Отправляем ответ
            await callback_query.message.answer(reply)
        except Exception as e:
            logging.error(f"Ошибка при загрузке данных о зале: {e}")
            await callback_query.message.answer("Произошла ошибка при загрузке данных о зале.")
    await callback_query.answer()



# ================= Команда /equipments =================
@dp.message(Command("equipments"))
async def choose_space_for_equipments(message: Message):
    async with aiohttp.ClientSession() as session:
        try:
            # Запрос списка залов
            async with session.get(DJANGO_API_BASE_URL + "spaces/") as response:
                if response.status == 200:
                    spaces = await response.json()
                    if spaces:
                        # Создаём клавиатуру с кнопками
                        keyboard = InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(
                                        text=space['name'],
                                        callback_data=f"equipments_space_{space['id']}"
                                    )
                                ]
                                for space in spaces
                            ]
                        )
                        await message.answer(
                            "Выберите зал для просмотра оборудования:",
                            reply_markup=keyboard
                        )
                    else:
                        await message.answer("Нет доступных залов.")
                else:
                    await message.answer("Ошибка при получении данных о залах.")
        except Exception as e:
            logging.error(f"Ошибка при запросе к API: {e}")
            await message.answer("Произошла ошибка при попытке получить данные о залах.")


@dp.callback_query(lambda c: c.data.startswith("equipments_space_"))
async def list_equipments_callback(callback_query):
    space_id = callback_query.data.split("_")[-1]
    async with aiohttp.ClientSession() as session:
        async with session.get(DJANGO_API_BASE_URL + f"equipments/?space_id={space_id}") as response:
            if response.status == 200:
                equipments = await response.json()
                if equipments:
                    reply = "Оборудование:\n"
                    for eq in equipments:
                        reply += f"- {eq['name']}: {eq.get('description', 'Описание отсутствует')}\n"
                    await bot.send_message(callback_query.from_user.id, reply)
                else:
                    await bot.send_message(callback_query.from_user.id, "Оборудование отсутствует.")
            else:
                await bot.send_message(callback_query.from_user.id, "Ошибка при получении данных об оборудовании.")
    await callback_query.answer()


# ================= Команда /parking =================
@dp.message(Command("parking"))
async def list_parkings(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(DJANGO_API_BASE_URL + "parkings/") as response:
            if response.status == 200:
                parkings = await response.json()
                if parkings:
                    reply = "Парковки:\n"
                    for parking in parkings:
                        is_paid = "Платная" if parking["is_paid"] else "Бесплатная"
                        price = f"{parking['price_per_hour']} BYN/час" if parking.get("price_per_hour") else ""
                        reply += f"{parking['name']} ({is_paid}) {price}\n"
                    await message.answer(reply)
                else:
                    await message.answer("Нет доступных парковок.")
            else:
                await message.answer("Ошибка при получении данных о парковках.")


# ================= Команда /book =================
@dp.message(Command("book"))
async def start_booking(message: Message, state: FSMContext):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(DJANGO_API_BASE_URL + "spaces/") as response:
                if response.status == 200:
                    spaces = await response.json()
                    if spaces:
                        keyboard = InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(
                                        text=space['name'],
                                        callback_data=f"select_space_{space['id']}"
                                    )
                                ]
                                for space in spaces
                            ]
                        )
                        await message.answer(
                            "Выберите зал для бронирования:",
                            reply_markup=keyboard
                        )
                        # Устанавливаем состояние FSM через set_state
                        await state.set_state(BookingState.waiting_for_space)
                    else:
                        await message.answer("Нет доступных залов.")
                else:
                    await message.answer(
                        f"Ошибка при получении данных о залах: {response.status}"
                    )
        except Exception as e:
            logging.error(f"Ошибка в процессе бронирования: {e}")
            await message.answer("Произошла ошибка при попытке получить данные о залах.")


@dp.callback_query(lambda c: c.data.startswith("select_space_"))
async def process_space_selection(callback_query, state: FSMContext):
    space_id = callback_query.data.split("_")[-1]
    await state.update_data(space_id=space_id)
    await bot.send_message(callback_query.from_user.id, "Введите ваше имя:")
    await state.set_state(BookingState.waiting_for_name)
    await callback_query.answer()


@dp.message(BookingState.waiting_for_name)
async def process_booking_name(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text)
    await message.answer("Введите ваш контакт (телефон или email):")
    await state.set_state(BookingState.waiting_for_contact)


@dp.message(BookingState.waiting_for_contact)
async def process_booking_contact(message: Message, state: FSMContext):
    await state.update_data(user_contact=message.text)
    await message.answer("Введите дату начала бронирования (в формате ГГГГ-ММ-ДД ЧЧ:ММ):")
    await state.set_state(BookingState.waiting_for_date)


@dp.message(BookingState.waiting_for_date)
async def process_booking_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer("Введите дату окончания бронирования (в формате ГГГГ-ММ-ДД ЧЧ:ММ):")
    await state.set_state(BookingState.waiting_for_end_date)


@dp.message(BookingState.waiting_for_end_date)
async def process_booking_end_date(message: Message, state: FSMContext):
    await state.update_data(end_date=message.text)

    # Проверка доступности зала
    data = await state.get_data()
    booking_payload = {
        "space": data["space_id"],
        "user_name": data["user_name"],
        "user_contact": data["user_contact"],
        "date": data["date"],
        "end_date": data["end_date"]
    }

    async with aiohttp.ClientSession() as session:
        try:
            # Проверяем существующие бронирования
            async with session.get(DJANGO_API_BASE_URL + "bookings/") as response:
                if response.status == 200:
                    bookings = await response.json()
                    conflicts = [
                        booking for booking in bookings
                        if booking["space"] == booking_payload["space"] and
                        not (
                            booking_payload["end_date"] <= booking["date"] or
                            booking_payload["date"] >= booking["end_date"]
                        )
                    ]

                    if conflicts:
                        await message.answer(
                            "Выбранное время уже занято. Попробуйте указать другой промежуток."
                        )
                        return

            # Создаём бронирование, если нет конфликтов
            async with session.post(DJANGO_API_BASE_URL + "bookings/", json=booking_payload) as response_post:
                if response_post.status in (200, 201):
                    await message.answer("Бронирование успешно создано!")
                else:
                    error_text = await response_post.text()
                    await message.answer(f"Ошибка при создании бронирования: {error_text}")

        except Exception as e:
            logging.error(f"Ошибка при проверке доступности: {e}")
            await message.answer("Произошла ошибка при проверке доступности зала.")

    await state.clear()



# ================= Запуск бота =================
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
