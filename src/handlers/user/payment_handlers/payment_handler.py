from bot import user_client
from telethon import events, types
import os
from dotenv import load_dotenv
from src.handlers.user import retutn_money_user, buying_succes, prolong_succes
from database import add_money, payment_succes, get_link, add_new_proxy, get_user, prolong_proxy_db
from APIS.proxy import buying_proxy

load_dotenv()



async def buying_mes(event: types.Message, payment_amount, payment_days, payment_user_id):
    result = await buying_proxy.buy_the_proxy(period=payment_days)
    if result[0] == "200":
        proxy_data = {} 
        resp_buy = result[1]
        proxy_data['price'] = resp_buy['price']
        proxy_data['user_id'] = payment_user_id
        proxy_data['country'] = resp_buy["country"]
        for prox in resp_buy['list']:
            for field in resp_buy["list"][prox]:
                proxy_data[field] = resp_buy["list"][prox][field]
        print(proxy_data)
        await add_new_proxy(proxy_data)
        user = await get_user(user_id=payment_user_id)
        await buying_succes(tg_id=user.tg_id, amount=payment_amount, id=proxy_data["id"])
    else:
        await add_money(user_id=payment_user_id, money=payment_amount)
        user = await get_user(user_id=payment_user_id)
        await retutn_money_user(tg_id=user.tg_id, amount=payment_amount)

async def prolong_mes(event: types.Message, payment_days, payment_user_id, payment_amount):
    result = await buying_proxy.prolong_proxy(payment_days)
    if result[0] == '200':
        resp_prolong = result[1]
        proxy_data = {} 
        for prox in resp_prolong['list']:
            proxy_data['id'] = prox
            for field in resp_prolong["list"][prox]:
                proxy_data[field] = resp_prolong["list"][prox][field]
        print(proxy_data)
        await prolong_proxy_db(proxy_data['id'], proxy_data['date_end'])
        user = await get_user(user_id=payment_user_id)
        await prolong_succes(tg_id=user.tg_id, amount=payment_amount, id=proxy_data["id"])
    else:
        await add_money(user_id=payment_user_id, money=payment_amount)
        user = await get_user(user_id=payment_user_id)
        await retutn_money_user(tg_id=user.tg_id, amount=payment_amount)


@user_client.on(events.NewMessage)
async def new_donors_messages(event: types.Message):
    handler_text = event.text
    if str(event.chat_id) == os.getenv("PAYMENT_CHAT_ID"):
        try:
            payment_id = handler_text.split()[2]
            await payment_succes(payment_id)
            payment = await get_link(payment_id)
            payment_amount = payment.amount
            payment_days = payment.days
            payment_user_id = payment.user_id
        except Exception as ex:
            print(f"Не то сообщение: {ex}")
            return
        link = await get_link(payment_id)
        if link.typ == 'buy':
            await buying_mes(event, payment_amount=payment_amount, payment_days=payment_days, payment_user_id=payment_user_id)
        if link.typ == 'prolong':
            await prolong_mes(event, payment_days=payment_days, payment_amount=payment_amount, payment_user_id=payment_user_id)


