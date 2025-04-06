from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiohttp import ClientSession
from ..config import logger
from ..keyboards import (
    create_finish_keyboard,
    create_contact_input_keyboard,
    create_promo_code_keyboard,
    create_finish_contact_keyboard,
    create_messengers_keyboard
)

API_URL = "http://127.0.0.1:8000/api/booking/"

router = Router()

# === Обработчики ввода контактных данных ===

@router.callback_query(lambda c: c.data == "start_contact_input")
async def start_contact_input(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Начинает процесс ввода контактных данных.
    """
    logger.info(f"Текущее состояние FSM: {await state.get_state()}")

    # Обновленное сообщение с эмодзи пера
    await callback_query.message.reply("✒️ Введите ваше имя:")
    await state.set_state("enter_name")



@router.message(StateFilter("enter_name"))
async def enter_name(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод имени.
    """
    logger.info(f"Имя введено: {message.text}")
    await state.update_data(name=message.text.strip())
    logger.info(f"Состояние после ввода имени: {await state.get_data()}")
    await message.reply("✒️ Введите ваш номер телефона:")
    await state.set_state("enter_phone")


@router.message(StateFilter("enter_phone"))
async def enter_phone(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод номера телефона.
    """
    logger.info(f"Телефон введён: {message.text}")
    await state.update_data(phone=message.text.strip())
    logger.info(f"Состояние после ввода телефона: {await state.get_data()}")
    await message.reply("✒️ Введите ваш email:")
    await state.set_state("enter_email")


@router.message(StateFilter("enter_email"))
async def enter_email(message: types.Message, state: FSMContext):
    """
    Обрабатывает ввод email.
    """
    logger.info(f"Email введён: {message.text.strip()}")

    await state.update_data(email=message.text.strip())
    logger.info(f"Состояние после ввода email: {await state.get_data()}")
    await message.reply(
        "✅ Контактные данные сохранены! Желаете ввести промокод?",
        reply_markup=create_promo_code_keyboard()
    )
    await state.set_state("promo_code_stage")


# === Обработчики промокода ===

@router.callback_query(lambda c: c.data == "enter_promo_code")
async def start_promo_code_input(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Начало ввода промокода.
    """
    logger.info(f"Начало ввода промокода. Текущее состояние FSM: {await state.get_state()}")

    await callback_query.message.reply("✒️ Пожалуйста, введите ваш промокод:")
    await state.set_state("enter_promo_code")


@router.message(StateFilter("enter_promo_code"))
async def enter_promo_code(message: types.Message, state: FSMContext):
    """
    Сохраняет введённый промокод.
    """
    logger.info(f"Промокод введён: {message.text.strip()}")
    await state.update_data(promo_code=message.text.strip())
    logger.info(f"Состояние после ввода промокода: {await state.get_data()}")

    await message.reply(
        "Теперь выберите мессенджер для связи:",
        reply_markup=create_messengers_keyboard()
    )
    await state.set_state("select_messenger_stage")


@router.callback_query(lambda c: c.data == "skip_promo_code")
async def skip_promo_code(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Пропускает ввод промокода.
    """
    logger.info("Промокод пропущен.")
    await callback_query.message.reply(
        "Вы пропустили ввод промокода. Теперь выберите мессенджер для связи:",
        reply_markup=create_messengers_keyboard()
    )
    await state.set_state("select_messenger_stage")


# === Обработчики выбора мессенджеров ===

@router.callback_query(lambda c: c.data.startswith("messenger:"))
async def select_messenger(callback_query: types.CallbackQuery, state: FSMContext):
    """
    Сохраняет выбранный мессенджер.
    """
    messenger = callback_query.data.split(":")[1]
    logger.info(f"Выбранный мессенджер: {messenger}")
    await state.update_data(messenger=messenger)
    logger.info(f"Состояние после выбора мессенджера: {await state.get_data()}")
    await callback_query.message.reply(
        "✅ Мессенджер сохранён! Завершите ввод данных.",
        reply_markup=create_finish_contact_keyboard()
    )
    await state.set_state("contact_input")


