from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from ..keyboards import create_calendar
from ..config import logger

# Создаём маршрутизатор
router = Router()

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
