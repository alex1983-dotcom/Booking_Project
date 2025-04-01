from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from ..config import logger, DJANGO_API_BASE_URL
from aiogram.filters import StateFilter
from aiohttp import ClientSession

router = Router()

# =======================Обработчик завершения бронирования ====================
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
