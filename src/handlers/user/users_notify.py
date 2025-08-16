from bot import bot

async def retutn_money_user(tg_id, amount):
    bot.send_message(tg_id, f"Что-то пошло не так, не удалось совершить операцию - {amount}руб. начислились на ваш баланс")