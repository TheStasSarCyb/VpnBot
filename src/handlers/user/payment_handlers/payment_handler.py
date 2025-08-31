from bot import user_client
from telethon import events, types
import os
import logging
from dotenv import load_dotenv
from src.handlers.user import retutn_money_user, buying_succes, prolong_succes
from database import add_money, payment_succes, get_link, add_new_proxy, get_user, prolong_proxy_db
from APIS.proxy import buying_proxy
from database.GG_table_api import make_table, make_table_wrong
from database.GG_table_api import make_table_prolong, make_table_prolong_wrong


load_dotenv()

limits = {
    '110': 7,
    '90': 7,
    '300': 30, 
    '560': 60, 
    '820': 90,
    '400': 30,
    '680': 60,
    '900': 90
}

# result1 = [200, {
#  "status": "yes",
#  "user_id": "1",
#  "balance": 42.5,
#  "currency": "RUB",
#  "order_id": 12345,
#  "count": 1,
#  "price": 6.3,
#  "period": 7,
#  "country": "ru",
#  "list": {
#    "300": {
#       "id": "300",
#       "ip": "2a00:1838:32:19f:45fb:2640::330",
#       "host": "185.22.134.250",
#       "port": "7330",
#       "user": "5svBNZ",
#       "pass": "iagn2d",
#       "type": "http",
#       "date": "2016-06-19 16:32:39",
#       "date_end": "2010-07-12 11:50:41",
#       "unixtime": 1466379159,
#       "unixtime_end": 1468349441,
#       "active": "1"
#    }
#  }
# }]

async def buying_mes(event: types.Message, payment_amount, payment_days, payment_user_id, link):
    if payment_amount in [110, 400, 680, 900]:
        version = 4
    else:
        version = 3
    if payment_amount in [110, 400, 680, 900]:
        if payment_amount == 110:
            payment_amount=90
        elif payment_amount == 400:
            payment_amount = 300
        elif payment_amount == 680:
            payment_amount = 560
        elif payment_amount == 900:
            payment_amount = 820
    result = await buying_proxy.buy_the_proxy(period=payment_days)
    if result[0] == 200:
        proxy_data = {} 
        resp_buy = result[1]
        proxy_data['ipv'] = version
        proxy_data['price_from_proxy'] = resp_buy['price']
        proxy_data['user_id'] = payment_user_id
        proxy_data['country'] = resp_buy["country"]
        for prox in resp_buy['list']:
            for field in resp_buy["list"][prox]:
                proxy_data[field] = resp_buy["list"][prox][field]
        logging.info(proxy_data)
        await make_table(proxy_data, link)
        proxy = await add_new_proxy(proxy_data)
        user = await get_user(user_id=payment_user_id)
        await buying_succes(tg_id=user.tg_id, amount=payment_amount, id=proxy_data["id"], proxy_data=proxy)
    else:
        await make_table_wrong(link)
        await add_money(user_id=payment_user_id, money=payment_amount)
        user = await get_user(user_id=payment_user_id)
        await retutn_money_user(tg_id=user.tg_id, amount=payment_amount)

# result2 = [200, {
#  "status": "yes",
#  "user_id": "1",
#  "balance": 29,
#  "currency": "RUB",
#  "order_id": 12345,
#  "price": 360,
#  "period": 7,
#  "count": 1,
#  "list": {
#    "21": {
#       "id": 21,
#       "date_end": "2024-07-15 06:30:27",
#       "unixtime_end": 1466379159
#    }
#  }
# }]

async def prolong_mes(event: types.Message, payment_days, payment_user_id, payment_amount, proxy_id, link):
    if payment_amount in [110, 400, 680, 900]:
        version = 4
    else:
        version = 3
    if payment_amount in [110, 400, 680, 900]:
        if payment_amount == 110:
            payment_amount=90
        elif payment_amount == 400:
            payment_amount = 300
        elif payment_amount == 680:
            payment_amount = 560
        elif payment_amount == 900:
            payment_amount = 820
    result = await buying_proxy.prolong_proxy(payment_days, proxy_id=proxy_id)
    if result[0] == 200:
        resp_prolong = result[1]
        proxy_data = {} 
        proxy_data['ipv'] = version
        for prox in resp_prolong['list']:
            proxy_data['id'] = prox
            for field in resp_prolong["list"][prox]:
                proxy_data[field] = resp_prolong["list"][prox][field]
        logging.info(proxy_data)
        await make_table_prolong(proxy_data, link)
        proxy = await prolong_proxy_db(proxy_data['id'], proxy_data['date_end'])
        user = await get_user(user_id=payment_user_id)
        await prolong_succes(tg_id=user.tg_id, amount=payment_amount, id=proxy_data["id"], proxy_data=proxy)
    else:
        await make_table_prolong_wrong(link)
        await add_money(user_id=payment_user_id, money=payment_amount)
        user = await get_user(user_id=payment_user_id)
        await retutn_money_user(tg_id=user.tg_id, amount=payment_amount)


@user_client.on(events.NewMessage)
async def new_donors_messages(event: types.Message):
    handler_text = event.text
    # logging.info(handler_text+'\n'+str(event.chat_id)+'\n'+str(os.getenv("PAYMENT_CHAT_ID")))
    if str(event.chat_id) == os.getenv("PAYMENT_CHAT_ID"):
        logging.info(handler_text+'\n'+str(event.chat_id)+'\n'+str(os.getenv("PAYMENT_CHAT_ID")))
        try:
            payment_id = handler_text.split()[2]
            payment_amount_com = float(handler_text.split()[-3])
            #if the payment actually succes? 
            await payment_succes(payment_id, amount_with_comission=payment_amount_com)
            payment = await get_link(payment_id)
            payment_amount = payment.amount
            payment_days = payment.days
            payment_user_id = payment.user_id
        except Exception as ex:
            logging.error(f"Не то сообщение: {ex}")
            return
        link = await get_link(payment_id)
        
        if link.typ == 'buy':
            await buying_mes(event, payment_amount=payment_amount, payment_days=payment_days, payment_user_id=payment_user_id, link = link)
        if link.typ == 'prolong':
            await prolong_mes(event, payment_days=payment_days, payment_amount=payment_amount, payment_user_id=payment_user_id, proxy_id=link.proxy_id, link = link)


