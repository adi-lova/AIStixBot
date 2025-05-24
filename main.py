import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import generate_sticker
from bot.config import load_config
from dotenv import load_dotenv

load_dotenv()

async def main():
    config = load_config(".env")
    bot = Bot(token=config.bot_token)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(generate_sticker.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())