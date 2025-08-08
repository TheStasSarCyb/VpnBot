import asyncio
from bot import bot, dp
from proxy import get_price

async def main():
    await dp.start_polling(bot)
    await get_price(count=100, period=10)


if __name__ == '__main__':
    asyncio.run(main())