import requests
from proxy.supporting_methods import ids_to_str, link

async def get_price(period: int="30", count: int='1') -> int:
    print(f"[get_price]: getting the price")
    response = requests.get(f"{link}/getprice?count={count}&period={period}&version=3")
    resullt = response.json()
    proxy_api_price = int(resullt.get("price", None))
    print(f"[get_price]: status: {response.status_code}\ndata: {resullt}")
    return proxy_api_price

async def buying_proxy(count: int, period: int, country="us"):
    response = requests.get(f"{link}buy?count={count}&period={period}&country={country}")
    data = response.json()
    print(response.status_code, data)

async def prolong_proxy(period: int, ids):
    str_ids = ids_to_str(ids)
    response = requests.get(f"{link}prolong?period={period}&ids={str_ids}")
    data = response.json()
    print(response.status(), data)