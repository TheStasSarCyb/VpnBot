import asyncio
from bot import bot, dp, user_client
from database import init_db
from src.handlers.user.payment_handlers import payment_handler

async def main():
    await init_db()

    # Сначала запускаем Telethon-клиент
    await user_client.start()  # ← дожидаемся полного подключения
    print("✅ Telethon-клиент успешно подключён")

    # Теперь запускаем всё вместе
    await asyncio.gather(
        dp.start_polling(bot),               # aiogram бот
        user_client.run_until_disconnected() # Telethon слушает события
    )

if __name__ == '__main__':
    asyncio.run(main())