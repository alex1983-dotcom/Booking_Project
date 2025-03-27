from aiogram import Dispatcher
from bot_booking import bot, storage, router

async def main():
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
