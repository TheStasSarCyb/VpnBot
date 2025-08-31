import asyncio
import logging

logging.basicConfig(level=logging.INFO, filename='LOGS.log', filemode='a', format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%d/%b/%Y %H:%M:%S")

from bot import bot, dp, user_client
from database import init_db, add_money, change, append_the_data
from src.handlers.user.payment_handlers import payment_handler
from database.models import migrate_db

async def main():
    await init_db()

    # Сначала запускаем Telethon-клиент
    await user_client.start()  # ← дожидаемся полного подключения
    logging.info("✅ Telethon-клиент успешно подключён")

    me = await user_client.get_me()

    logging.info(me)
    # Теперь запускаем всё вместе
    await asyncio.gather(
        dp.start_polling(bot),               # aiogram бот
        user_client.run_until_disconnected() # Telethon слушает события
    )



if __name__ == '__main__':
    asyncio.run(main())