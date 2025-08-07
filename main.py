from aiogram import Dispatcher
from aiogram.types import Message
from config import bot
import asyncio

from app.han

async def main():
    dp = Dispatcher()
    dp.include_router(router)

if __name__ == '__main__':
    asyncio.run(main())