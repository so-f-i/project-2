import asyncio
from aiogram import Bot, Dispatcher
from config.settings import BOT_TOKEN
from utils.logger import logger
from routers import commands
from routers import mood_fsm
from routers import admin_panel
from aiogram.fsm.storage.memory import MemoryStorage

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
# dp = Dispatcher()
dp.include_router(commands.router)
dp.include_router(admin_panel.router)
dp.include_router(mood_fsm.router)

async def main():
    logger.info("Запуск бота")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Ошибка во время работы бота: {e}")

if __name__ == "__main__":
    asyncio.run(main())
