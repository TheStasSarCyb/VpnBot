import requests
from APIS.proxy.supporting_methods import ids_to_str, link

async def get_count_of_proxy(country: str='us'):
    print(f"[get_count_of_proxy]: getting:\ncountry: {country}")
    response = requests.get(f"{link}/getcount?country={country}&version=3")
    resullt = response.json()
    print(f"[get_count_of_proxy]: status: {response.status_code}\ndata: {resullt}")
    return resullt['count']

async def buy_the_proxy(period: int, count: int=1, country="us"):
    print(f"[buying_proxy]: buying:\n count: {count}, period: {period}, country: {country}")
    response = requests.get(f"{link}/buy?count={count}&period={period}&country={country}&version=3")
    resullt = response.json()
    print(f"[buying_proxy]: status: {response.status_code}\ndata: {resullt}")
    return [response.status_code, resullt]

async def prolong_proxy(period: int, ids):
    str_ids = ids_to_str(ids)
    print(f"[prolonging_proxy]: prolong:/n period: {period}, ids: {str_ids}")
    response = requests.get(f"{link}/prolong?period={period}&ids={str_ids}")
    resullt = response.json()
    print(f"[prolong_proxy]: status: {response.status_code}\ndata: {resullt}")