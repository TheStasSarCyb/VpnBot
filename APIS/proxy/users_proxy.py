import requests
from proxy.supporting_methods import ids_to_str, link

async def check_proxy(ids):
    str_ids = ids_to_str(ids)
    print(f"[check_proxy]: \nchecking: {str_ids}")
    response = await requests.get(f"{link}check?ids={str_ids}")
    resullt = response.json()
    print(f"[check_proxy]: status: {response.status_code}\ndata: {resullt}")

async def delete_proxy(ids):
    str_ids = ids_to_str(ids)
    print(f"[delete_proxy]: \ndeleting: {str_ids}")
    response = await requests.get(f"{link}delete?ids={str_ids}")
    resullt = response.json()
    print(f"[delete_proxy]: status: {response.status_code}\ndata: {resullt}")

async def get_all_proxy():
    response = await requests.get(f"{link}getproxy")
    resullt = response.json()
    print(f"[get_all_proxy]: status: {response.status_code}\ndata: {resullt}")
