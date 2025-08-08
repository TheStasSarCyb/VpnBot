import time
import hmac
import hashlib
import json
import requests

import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("FREEKASSA_TOKEN")
shop_id = os.getenv("SHOP_ID")

def generate_new_link(amount: int, id_: int):
    data = {
    'shopId': shop_id,
    'nonce': int(time.time()),
    'i': id_,
    'email': "karagaj@ya.ru",
    'ip': "162.158.94.55",
    'amount': amount,
    'currency': "RUB",
    }
    sorted_data = dict(sorted(data.items()))
    values_str = '|'.join(str(value) for value in sorted_data.values())
    sign = hmac.new(token.encode('utf-8'), values_str.encode('utf-8'), hashlib.sha256).hexdigest()
    sorted_data['signature'] = sign
    request = json.dumps(sorted_data)

    response = requests.post(url, data=request)

    payment_data = response.json()
    return [str(current_count+1), payment_data]