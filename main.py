import asyncio
from bot import bot, dp, user_client
from database import init_db

async def main():
    await dp.start_polling(bot)
    await user_client.run_until_disconnected()
    await init_db()

if __name__ == '__main__':
    asyncio.run(main())