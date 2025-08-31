from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from database import get_user, get_all_links, get_proxy
from APIS.proxy import users_proxy
import logging

sheet_id = "1oDC6C6nevnFZOuBuDqQVANFataENRg1Jivh8dI2aBH4"

# Путь к твоему JSON-файлу учетной записи
SCOPES = ['https://www.googleapis.com/auth/spreadsheets'] 
SERVICE_ACCOUNT_FILE = 'apis2.json'  # замени на свой путь

# Аутентификация
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Инициализация сервиса
service = build('sheets', 'v4', credentials=credentials)

current_data = {}

async def make_table(proxy_date, link):
    mas = []
    # tg_id,
    user_id = proxy_date['user_id']
    user = await get_user(user_id=int(user_id))
    tg_id = user.tg_id
    mas.append(tg_id)
    # Username,
    username = user.username
    mas.append(username)
    # id_,
    id_ = proxy_date['id']
    mas.append(id_)
    # protocol,
    # protocol = proxy_date['type']
    # mas.append(protocol)
    # ip,
    # ip = proxy_date["host"]
    # mas.append(ip)
    # user_auth,
    # user_auth = proxy_date["user"]
    # mas.append(user_auth)
    # password,
    # password = proxy_date["pass"]
    # mas.append(password)
    # port,
    # port = proxy_date["port"]
    # mas.append(port)
    # country,
    # country = proxy_date['country']
    # mas.append(country)
    # date,
    # date = proxy_date["date"]
    # mas.append(date)
    # date_end,
    # date_end = proxy_date["date_end"]
    # mas.append(date_end)
    # ipv,
    # ipv = proxy_date['ipv']
    # mas.append(ipv)
    # typ
    mas.append("buy")
    # price_from_proxy,
    price_from_proxy = proxy_date["price_from_proxy"]
    mas.append(price_from_proxy)
    # our_price,
    # last_link = await get_all_links(user_id)
    our_price = link.amount
    if our_price in [110, 400, 680, 900]:
        if our_price == 110:
            our_price=90
        elif our_price == 400:
            our_price = 300
        elif our_price == 680:
            our_price = 560
        elif our_price == 900:
            our_price = 820
    mas.append(our_price)
    # our_price_with_comission,
    our_price_with_comission = link.amount_with_comission
    mas.append(our_price_with_comission)
    # difference,
    difference = our_price_with_comission - price_from_proxy
    mas.append(difference)
    # developers_fraction,
    developers_fraction = 0.3*(difference)
    mas.append(developers_fraction)
    # owners_fraction
    owners_fraction = 0.7*(difference)
    mas.append(owners_fraction)

    await append_the_data(mas)

async def make_table_prolong(proxy_date, link):
    mas = []
    # id_,
    id_ = proxy_date['id']
    # tg_id,
    logging.info(str(id_))
    proxy = await get_proxy(id_=id_)
    user_id = proxy.user_id
    user = await get_user(user_id=int(user_id))
    tg_id = user.tg_id
    mas.append(tg_id)
    # Username,
    username = user.username
    mas.append(username)
    mas.append(id_)
    # protocol,
    # protocol = proxy.protocol
    # mas.append(protocol)
    # ip,
    # ip = proxy.ip
    # mas.append(ip)
    # user_auth,
    # user_auth = proxy.user_auth
    # mas.append(user_auth)
    # password,
    # password = proxy.password
    # mas.append(password)
    # port,
    # port = proxy.port
    # mas.append(port)
    # country,
    # country = proxy.country
    # mas.append(country)
    # date,
    # date = proxy.date
    # mas.append(date)
    # date_end,
    # date_end = proxy.date_end
    # mas.append(date_end)
    # ipv,
    # ipv = proxy.ipv
    # mas.append(ipv)
    # price_from_proxy,
    # typ
    mas.append("prolong")
    if link.amount in [110, 400, 680, 900]:
        version = 4
    else:
        version = 3

    if link.amount in [400, 300]:
        period = 30
    elif link.amount in [90, 110]:
        period = 7
    elif link.amount in [560, 680]:
        period = 60
    elif link.amount in [900, 820]:
        period = 90
    
    price_from_proxy = await users_proxy.get_price(version=version, period=period)
    mas.append(price_from_proxy)
    # our_price,
    # all_links = await get_all_links(user_id)
    # last_link = all_links[-1]
    our_price = link.amount
    if our_price in [110, 400, 680, 900]:
        if our_price == 110:
            our_price=90
        elif our_price == 400:
            our_price = 300
        elif our_price == 680:
            our_price = 560
        elif our_price == 900:
            our_price = 820
    mas.append(our_price)
    # our_price_with_comission,
    our_price_with_comission = link.amount_with_comission
    mas.append(our_price_with_comission)
    # difference,
    difference = our_price_with_comission - price_from_proxy
    mas.append(difference)
    # developers_fraction,
    developers_fraction = 0.3*(difference)
    mas.append(developers_fraction)
    # owners_fraction
    owners_fraction = 0.7*(difference)
    mas.append(owners_fraction)

    await append_the_data(mas)

async def make_table_wrong(link):
    mas = []
    # tg_id,
    user_id = link.user_id
    user = await get_user(user_id=int(user_id))
    tg_id = user.tg_id
    mas.append(tg_id)
    # Username,
    username = user.username
    mas.append(username)
    # id_,
    mas.append('')
    # typ
    mas.append("buy")
    # price_from_proxy,

    # тут буду кидать запрос
    if link.amount in [110, 400, 680, 900]:
        version = 4
    else:
        version = 3

    if link.amount in [400, 300]:
        period = 30
    elif link.amount in [90, 110]:
        period = 7
    elif link.amount in [560, 680]:
        period = 60
    elif link.amount in [900, 820]:
        period = 90
    
    price_from_proxy = await users_proxy.get_price(version=version, period=period)
    mas.append(price_from_proxy)

    # our_price,
    # last_link = await get_all_links(user_id)
    our_price = link.amount
    if our_price in [110, 400, 680, 900]:
        if our_price == 110:
            our_price=90
        elif our_price == 400:
            our_price = 300
        elif our_price == 680:
            our_price = 560
        elif our_price == 900:
            our_price = 820
    mas.append(our_price)
    # our_price_with_comission,
    our_price_with_comission = link.amount_with_comission
    mas.append(our_price_with_comission)
    # difference,
    difference = our_price_with_comission - price_from_proxy
    mas.append(difference)
    # developers_fraction,
    developers_fraction = 0.3*(difference)
    mas.append(developers_fraction)
    # owners_fraction
    owners_fraction = 0.7*(difference)
    mas.append(owners_fraction)

    await append_the_data(mas)

async def make_table_prolong_wrong(link):
    mas = []
    # tg_id,
    user_id = link.user_id
    user = await get_user(user_id=int(user_id))
    tg_id = user.tg_id
    mas.append(tg_id)
    # Username,
    username = user.username
    mas.append(username)
    # id_,
    mas.append('')
    # typ
    mas.append("prolong")
    # price_from_proxy,
    # тут буду кидать запрос
    
    if link.amount in [110, 400, 680, 900]:
        version = 4
    else:
        version = 3

    if link.amount in [400, 300]:
        period = 30
    elif link.amount in [90, 110]:
        period = 7
    elif link.amount in [560, 680]:
        period = 60
    elif link.amount in [900, 820]:
        period = 90
    
    price_from_proxy = await users_proxy.get_price(version=version, period=period)
    mas.append(price_from_proxy)
    # our_price,
    # last_link = await get_all_links(user_id)
    our_price = link.amount
    if our_price in [110, 400, 680, 900]:
        if our_price == 110:
            our_price=90
        elif our_price == 400:
            our_price = 300
        elif our_price == 680:
            our_price = 560
        elif our_price == 900:
            our_price = 820
    mas.append(our_price)
    # our_price_with_comission,
    our_price_with_comission = link.amount_with_comission
    mas.append(our_price_with_comission)
    # difference,
    difference = our_price_with_comission - price_from_proxy
    mas.append(difference)
    # developers_fraction,
    developers_fraction = 0.3*(difference)
    mas.append(developers_fraction)
    # owners_fraction
    owners_fraction = 0.7*(difference)
    mas.append(owners_fraction)

    await append_the_data(mas)


# Выполняем append
async def append_the_data(array_data: list):
    request = service.spreadsheets().values().append(
        spreadsheetId=sheet_id,
        range="List1",  # Можно указать точный диапазон, например: "Лист1!A:E"
        valueInputOption='USER_ENTERED',
        body={'values': [array_data]}
    ).execute()
    
    return request

def get_last_raw():
    request = service.spreadsheets().values().get(spreadsheetId=sheet_id, range="List1!A:A").execute()
    values = request.get("values", [])
    last_raw = len(values) + 1
    return last_raw

# logging.info(get_last_raw())