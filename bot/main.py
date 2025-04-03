import asyncio
from aiogram import Dispatcher
from bot_booking import bot, storage
from bot_booking.handlers import routers
from bot_booking.config import logger

async def main():
    try:
        dp = Dispatcher(storage=storage)

        # Регистрация всех маршрутизаторов
        for router in routers:
            dp.include_router(router)

        logger.info("Бот успешно запущен.")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске: {e}")
    finally:
        await bot.session.close()
        logger.info("Сессия завершена.")

if __name__ == "__main__":
    asyncio.run(main())
