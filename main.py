import asyncio
from bot import bot, dp, user_client
from database import init_db, check_tables

async def main():
    await init_db()
    await user_client.run_until_disconnected()
    await dp.start_polling(bot)
   
    
    

if __name__ == '__main__':
    asyncio.run(main())