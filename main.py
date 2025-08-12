import asyncio
from bot import bot, dp, user_client

async def main():
    await dp.start_polling(bot)
    await user_client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())