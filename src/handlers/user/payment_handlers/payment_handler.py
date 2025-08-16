from bot import user_client
from telethon import events, types
import os
from dotenv import load_dotenv
from database import payment_succes, get_link, add_new_proxy
from APIS.proxy import buying_proxy

load_dotenv()

resp = {
 "status": "yes",
 "user_id": "1",
 "balance": 42.5,
 "currency": "RUB",
 "count": 1,
 "price": 6.3,
 "period": 7,
 "country": "ru",
 "list": {
   "15": {
      "id": "15",
      "ip": "2a00:1838:32:19f:45fb:2640::330",
      "host": "185.22.134.250",
      "port": "7330",
      "user": "5svBNZ",
      "pass": "iagn2d",
      "type": "http",
      "date": "2016-06-19 16:32:39",
      "date_end": "2016-07-12 11:50:41",
      "unixtime": 1466379159,
      "unixtime_end": 1468349441,
      "active": "1"
   }
 }
}

@user_client.on(events.NewMessage)
async def new_donors_messages(event: types.Message):
    handler_text = event.text

    if event.chat_id == os.getenv("PAYMENT_CHAT_ID"):
        try:
            payment_id = handler_text.split()[2]
            await payment_succes(payment_id)
            payment = await get_link(payment_id)
            payment_days = payment.days
            payment_user_id = payment.user_id

            status, purchased_proxy = await buying_proxy.buy_the_proxy(period=int(payment_days))
            if status == 200:
                print(f"[new_donors_messages](status 200): is adding...")
                await add_new_proxy(purchased_proxy, payment_user_id)
            else:
                print(f"[new_donors_messages](status {status}): error is {purchased_proxy}") # если что, purchased_proxy покажет контент ошибки, так что всё ок

            # await add_proxy(payment_days, payment_user_id)
            for prox in resp['list']:
                for field in resp["list"][prox]:
                    print(resp["list"][prox][field])
        except Exception as ex:
            print("Не то сообщение")
        
        # result = await buying_proxy(1, payment_days)
        # if result[0] == "200":

        # else:

