import asyncio
from bot import bot, dp, user_client
from database import init_db, check_tables

async def main():
    await init_db()
    await dp.start_polling(bot)
    await user_client.run_until_disconnected()
    
    

if __name__ == '__main__':
    asyncio.run(main())