import requests
import logging
from APIS.proxy.supporting_methods import ids_to_str, link


async def check_proxy(ids):
    str_ids = ids_to_str(ids)
    logging.info(f"[check_proxy]: \nchecking: {str_ids}")
    response = await requests.get(f"{link}check?ids={str_ids}")
    resullt = response.json()
    logging.info(f"[check_proxy]: status: {response.status_code}\ndata: {resullt}")

async def delete_proxy(ids):
    str_ids = ids_to_str(ids)
    logging.info(f"[delete_proxy]: \ndeleting: {str_ids}")
    response = await requests.get(f"{link}delete?ids={str_ids}")
    resullt = response.json()
    logging.info(f"[delete_proxy]: status: {response.status_code}\ndata: {resullt}")

async def get_all_proxy():
    response = await requests.get(f"{link}getproxy")
    resullt = response.json()
    logging.info(f"[get_all_proxy]: status: {response.status_code}\ndata: {resullt}")

async def get_price(version, period, count=1):
    response = requests.get(f"{link}/getprice?count={count}&period={period}&version={3}")
    resullt = response.json()
    logging.info(str(resullt))
    return resullt['price']
