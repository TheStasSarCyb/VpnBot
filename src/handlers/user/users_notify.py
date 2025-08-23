from bot import bot

async def retutn_money_user(tg_id, amount):
    await bot.send_message(chat_id=tg_id, text=f"Что-то пошло не так, не удалось совершить операцию - {amount}руб. начислились на ваш баланс")

async def buying_succes(tg_id, amount, id):
    await bot.send_message(chat_id=tg_id, text=f"Оплата в размере {amount}RUB прошла успешно\nПрокси с id {id} добавлен в ваши прокси")

async def prolong_succes(tg_id, amount, id):
    await bot.send_message(chat_id=tg_id, text=f"Оплата в размере {amount}RUB прошла успешно\nПрокси с id {id} продлён")