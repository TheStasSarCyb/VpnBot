from bot import bot

async def retutn_money_user(tg_id, amount):
    await bot.send_message(chat_id=tg_id, text=f"Что-то пошло не так, не удалось совершить операцию - {amount}руб. начислились на ваш баланс")

async def buying_succes(tg_id, amount, id, proxy_data):

    str_proxies = "<b>id прокси: </b>" + str(proxy_data.id_)+'\n'
    str_proxies += '<b>ip: </b>' + str(proxy_data.ip) + '\n'
    str_proxies += '<b>port: </b>' + str(proxy_data.port) + '\n'
    str_proxies += '<b>логин: </b>' + str(proxy_data.user_auth) + '\n'
    str_proxies += '<b>пароль: </b>' + str(proxy_data.password) + '\n'
    str_proxies += '<b>дата начала прокси: </b>' + str(proxy_data.date) + '\n'
    str_proxies += '<b>дата истечения прокси: </b>' + str(proxy_data.date_end) + '\n'
    str_proxies += '<b>протокол: </b>' + str(proxy_data.protocol) +'\n'
    await bot.send_message(chat_id=tg_id, text=f"Оплата в размере {amount}RUB прошла успешно\n{str_proxies}", parse_mode='HTML')

async def prolong_succes(tg_id, amount, id, proxy_data):
    str_proxies = "<b>id прокси: </b>" + str(proxy_data.id_)+'\n'
    str_proxies += '<b>ip: </b>' + str(proxy_data.ip) + '\n'
    str_proxies += '<b>port: </b>' + str(proxy_data.port) + '\n'
    str_proxies += '<b>логин: </b>' + str(proxy_data.user_auth) + '\n'
    str_proxies += '<b>пароль: </b>' + str(proxy_data.password) + '\n'
    str_proxies += '<b>дата начала прокси: </b>' + str(proxy_data.date) + '\n'
    str_proxies += '<b>дата истечения прокси: </b>' + str(proxy_data.date_end) + '\n'
    str_proxies += '<b>протокол: </b>' + str(proxy_data.protocol) +'\n'
    await bot.send_message(chat_id=tg_id, text=f"Оплата в размере {amount}RUB прошла успешно, прокси продлён\n{str_proxies}", parse_mode='HTML')