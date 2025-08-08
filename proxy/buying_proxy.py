import requests
from proxy.supporting_methods import ids_to_str, link

async def get_price(count: int, period: int, version: int):
    response = await requests.get(link+'getprice?count='+count+'&period='+period)
    data = response.json()
    print(response.status(), data)

async def buying_proxy(count: int, period: int, version: int, type = "http", country = "us"):
    response = await requests.get(f"{link}buy?count={count}&period={period}&country={country}")
    data = response.json()
    print(response.status(), data)

async def prolong_proxy(period: int, ids):
    str_ids = ids_to_str(ids)
    response = await requests.get(f"{link}prolong?period={period}&ids={str_ids}")
    data = response.json()
    print(response.status(), data)