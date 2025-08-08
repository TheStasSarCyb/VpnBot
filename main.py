import asyncio
from bot import bot, dp
from proxy.buying_proxy import get_price

async def main():
    await dp.start_polling(bot)
    get_price(count=5, period=10)


if __name__ == '__main__':
    asyncio.run(main())