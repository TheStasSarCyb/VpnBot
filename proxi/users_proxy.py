import requests
from supporting_methods import ids_to_str, link

async def get_price(count: int, period: int, version: int):
    response = await requests.get(link+'getprice?count='+count+'&period='+period)
    data = response.json()
    print(response.status(), data)

async def check_proxy(ids):
    str_ids = ids_to_str(ids)
    response = await requests.get(f"{link}check?ids={str_ids}")
    data = response.json()
    print(response.status(), data)

async def delete_proxy(ids):
    str_ids = ids_to_str(ids)
    response = await requests.get(f"{link}delete?ids={str_ids}")
    data = response.json()
    print(response.status(), data)