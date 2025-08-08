import asyncio
from bot import bot, dp
from proxy import get_price

async def main():
    proxy_api_price = await get_price(period=60)
    print(proxy_api_price)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())