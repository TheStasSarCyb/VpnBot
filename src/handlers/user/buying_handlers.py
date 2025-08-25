from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards import keyboards
from texts import texts
from texts import enums
from APIS.proxy import buying_proxy
from APIS.freekassa import generate_new_link
from src.fsm_scripts import fsm_lists, FSMContext
from database import User, Link, Proxy, async_session, add_user_and_pay, get_user, substract_money, add_new_proxy, add_money
from sqlalchemy import select, update, delete, func
from src.handlers.user.users_notify import retutn_money_user, buying_succes
router = Router()

prices = {
    "30": 300,
    "60": 560,
    "90": 820
}

@router.callback_query(fsm_lists.Buy.limit_time)
@router.callback_query(F.data.startswith("bying_proxy_"))
async def applicate_prices(callback: CallbackQuery, state: FSMContext):
    data = callback.data # CALLBACK

    await callback.answer(f"Прокси выбран")

    if data == enums.Bying_enum.days_30.value:
        await callback.message.answer('Вы выбрали "Купить прокси на 30 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_method_buttons) # TEXT CALLBACK

        await state.update_data(limit_time=30) # STATE
        await state.set_state(fsm_lists.Buy.pay_method) # STATE

    elif data == enums.Bying_enum.days_60.value:
        await callback.message.answer('Вы выбрали "Купить прокси на 60 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_method_buttons) # TEXT CALLBACK')

        await state.update_data(limit_time=60) # STATE
        await state.set_state(fsm_lists.Buy.pay_method) # STATE

    elif data == enums.Bying_enum.days_90.value:
        await callback.message.answer('Вы выбрали "Купить прокси на 90 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_method_buttons) # TEXT CALLBACK')

        await state.update_data(limit_time=90) # STATE
        await state.set_state(fsm_lists.Buy.pay_method) # STATE

@router.callback_query(F.data.in_(["ACC", "SBP", "CARD"]))
async def pay_method_handler(callback: CallbackQuery, state: FSMContext):
    data = callback.data # CALLBACK

    state_data = await state.get_data() # STATE
    limit_time = state_data['limit_time'] # STATE

    amount = prices[str(limit_time)]

    if data == enums.Pay_methods.ACC.value:
        await callback.answer("Метод оплаты выбран")
        user = await get_user(tg_id=callback.from_user.id)
        if user.money >= amount:
            await callback.message.answer(f"У вас {user.money}RUB\nМожно оплатить прокси, списав с баланса\nСписать {amount}RUB?", reply_markup=keyboards.account_money_pay)
            return

    await callback.answer(f"Метод оплаты выбран")
    if data == enums.Pay_methods.SBP.value:
        link = generate_new_link(amount=limit_time, pay_method=enums.Pay_methods.SBP.value)
        await callback.message.answer(f"Метод оплаты: {enums.Pay_methods.SBP.value}\nК оплате: {amount}RUB\nСсылка для оплаты: {link}\nПосле оплаты, вы получите ip и логин для подключения прокси сервера")

    elif data == enums.Pay_methods.CARD.value:
        link = generate_new_link(amount=limit_time, pay_method=enums.Pay_methods.CARD.value)
        await callback.message.answer(f"Метод оплаты: {enums.Pay_methods.CARD.value}\nК оплате: {amount}RUB\nСсылка для оплаты: {link}\nПосле оплаты, вы получите ip и логин для подключения прокси сервера")
    await add_user_and_pay(tg_id=callback.from_user.id, id=link.split('/')[-2], amount=amount, username=callback.from_user.full_name, typ="buy")
    
@router.callback_query(F.data.startswith('bonuses'))
async def acc_payment(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Оплата прошла")

    state_data = await state.get_data() # STATE
    limit_time = state_data['limit_time'] # STATE

    amount = prices[str(limit_time)]

    user = await substract_money(money=amount, tg_id=callback.from_user.id)
    
    await buying_mes(payment_amount=amount, payment_days=limit_time, payment_user_id=user.id)

async def buying_mes(payment_amount, payment_days, payment_user_id):
    result = await buying_proxy.buy_the_proxy(period=payment_days)
    if result[0] == "200":
        resp_buy = result[1]
        proxy_data = {} 
        proxy_data['price'] = resp_buy['price']
        proxy_data['user_id'] = payment_user_id
        proxy_data['country'] = resp_buy["country"]
        for prox in resp_buy['list']:
            for field in resp_buy["list"][prox]:
                proxy_data[field] = resp_buy["list"][prox][field]
        print(proxy_data)
        await add_new_proxy(proxy_data)
        user = await get_user(user_id=payment_user_id)
        await buying_succes(tg_id=user.tg_id, amount=payment_amount, id=proxy_data["id"])
    else:
        await add_money(user_id=payment_user_id, money=payment_amount)
        user = await get_user(user_id=payment_user_id)
        await retutn_money_user(tg_id=user.tg_id, amount=payment_amount)

@router.message(F.text == texts.MAIN_BUTTON_1)
async def applicate_prices(message: Message, state: FSMContext):
    await state.set_state(fsm_lists.Buy.limit_time)

    count_of_proxy = await buying_proxy.get_count_of_proxy()
    
    if count_of_proxy < 8:
        await message.answer(f"Доступных прокси слишком мало, покупка прокси пока недоступна")
    else:
        await message.answer(f"Доступных прокси: {count_of_proxy}")
        await message.answer(texts.PROXY_VIEW_1, reply_markup=keyboards.buy_proxy_1)
        await message.answer(texts.PROXY_VIEW_2, reply_markup=keyboards.buy_proxy_2)
        await message.answer(texts.PROXY_VIEW_3, reply_markup=keyboards.buy_proxy_3)