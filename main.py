import asyncio
from bot import bot, dp
from proxy.buying_proxy import get_price

async def main():
    await get_price(count=5, period=10)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())