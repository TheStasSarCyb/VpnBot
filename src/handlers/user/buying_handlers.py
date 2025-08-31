from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards import keyboards
from texts import texts
import logging
from texts import enums
from APIS.proxy import buying_proxy
from APIS.freekassa import generate_new_link
from src.fsm_scripts import fsm_lists, FSMContext
from database import User, Link, Proxy, async_session, add_user_and_pay, get_user, substract_money, add_new_proxy, add_money
from sqlalchemy import select, update, delete, func
from src.handlers.user.users_notify import retutn_money_user, buying_succes
from src.handlers.deleting_messages import add, clear
from database.GG_table_api import make_table_wrong
router = Router()

prices = {
    '7': 90,
    '8': 110,
    "30": 300,
    "60": 560,
    "90": 820,
    "31": 400,
    "61": 680,
    "91": 900
}



@router.callback_query(F.data.startswith("bying_proxy_"))
async def applicate_prices(callback: CallbackQuery, state: FSMContext):
    data = callback.data # CALLBACK

    await callback.answer(f"Прокси выбран")

    if data == enums.Bying_enum.days_pc_30.value:
        mes = await callback.message.answer('Вы выбрали "Купить прокси для пк на 30 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_method_buttons) # TEXT CALLBACK

        await state.update_data(limit_time=30) # STATE
        await state.set_state(fsm_lists.Buy.pay_method) # STATE
    elif data == enums.Bying_enum.days_pc_7.value:
        mes = await callback.message.answer('Вы выбрали "Купить прокси для пк на 7 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_method_buttons) # TEXT CALLBACK

        await state.update_data(limit_time=7) # STATE
        await state.set_state(fsm_lists.Buy.pay_method) # STATE
    elif data == enums.Bying_enum.days_pc_60.value:
        mes = await callback.message.answer('Вы выбрали "Купить прокси для пк на 60 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_method_buttons) # TEXT CALLBACK')

        await state.update_data(limit_time=60) # STATE
        await state.set_state(fsm_lists.Buy.pay_method) # STATE

    elif data == enums.Bying_enum.days_pc_90.value:
        mes = await callback.message.answer('Вы выбрали "Купить прокси для пк на 90 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_method_buttons) # TEXT CALLBACK')

        await state.update_data(limit_time=90) # STATE
        await state.set_state(fsm_lists.Buy.pay_method) # STATE

    elif data == enums.Bying_enum.days_phone_30.value:
        mes = await callback.message.answer('Вы выбрали "Купить прокси для телефона на 30 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_method_buttons) # TEXT CALLBACK')

        await state.update_data(limit_time=31) # STATE
        await state.set_state(fsm_lists.Buy.pay_method) # STATE

    elif data == enums.Bying_enum.days_phone_60.value:
        mes = await callback.message.answer('Вы выбрали "Купить прокси для телефона на 60 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_method_buttons) # TEXT CALLBACK')

        await state.update_data(limit_time=61) # STATE
        await state.set_state(fsm_lists.Buy.pay_method) # STATE

    elif data == enums.Bying_enum.days_phone_90.value:
        mes = await callback.message.answer('Вы выбрали "Купить прокси для телефона на 90 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_method_buttons) # TEXT CALLBACK')

        await state.update_data(limit_time=91) # STATE
        await state.set_state(fsm_lists.Buy.pay_method) # STATE
    
    elif data == enums.Bying_enum.days_phone_7.value:
        mes = await callback.message.answer('Вы выбрали "Купить прокси для телефона на 7 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_method_buttons) # TEXT CALLBACK')

        await state.update_data(limit_time=8) # STATE
        await state.set_state(fsm_lists.Buy.pay_method) # STATE

    if mes:
        await clear(int(callback.from_user.id))
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))

@router.callback_query(F.data.in_(["ACC", "SBP", "CARD"]))
async def pay_method_handler(callback: CallbackQuery, state: FSMContext):
    data = callback.data # CALLBACK

    state_data = await state.get_data() # STATE
    limit_time = state_data['limit_time'] # STATE

    true_amount = prices[str(limit_time)]

    if int(limit_time) in [8, 31, 61, 91]:
        limit_time-=1

    user_amount = prices[str(limit_time)]

    if data == enums.Pay_methods.ACC.value:
        await callback.answer("Метод оплаты выбран")
        user = await get_user(tg_id=callback.from_user.id)
        if user.money >= user_amount:
            msg = await callback.message.answer(f"У вас {user.money}RUB\nМожно оплатить прокси, списав с баланса\nСписать {user_amount}RUB?", reply_markup=keyboards.account_money_pay)
            await clear(int(callback.from_user.id))
            add(user_id=int(callback.from_user.id), msg_id=int(msg.message_id))
        else:
            msg = await callback.message.answer(f"У вас на балансе недостаточно средств")
            await clear(int(callback.from_user.id))
            add(user_id=int(callback.from_user.id), msg_id=int(msg.message_id))
        return
        

    await callback.answer(f"Метод оплаты выбран")
    if data == enums.Pay_methods.SBP.value:
        link = generate_new_link(amount=user_amount, pay_method=enums.Pay_methods.SBP.value)
        mes = await callback.message.answer(f"Метод оплаты: {enums.Pay_methods.SBP.value}\nК оплате: {user_amount}RUB\nСсылка для оплаты: {link}\nПосле оплаты, вы получите ip и логин для подключения прокси сервера")

    elif data == enums.Pay_methods.CARD.value:
        link = generate_new_link(amount=user_amount, pay_method=enums.Pay_methods.CARD.value)
        mes = await callback.message.answer(f"Метод оплаты: {enums.Pay_methods.CARD.value}\nК оплате: {user_amount}RUB\nСсылка для оплаты: {link}\nПосле оплаты, вы получите ip и логин для подключения прокси сервера")
    if mes:
        await clear(int(callback.from_user.id))
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))
    await add_user_and_pay(tg_id=callback.from_user.id, id=link.split('/')[-2], amount=true_amount, username=callback.from_user.full_name, typ="buy")
    
@router.callback_query(F.data.startswith('bonuses'))
async def acc_payment(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Оплата проходит")
    mes = await callback.message.answer("Ожидайте")

    await clear(int(callback.from_user.id))
    add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))

    state_data = await state.get_data() # STATE
    limit_time = state_data['limit_time'] # STATE

    true_amount = prices[str(limit_time)]

    if int(limit_time) in [8, 31, 61, 91]:
        limit_time = int(limit_time)-1

    user_amount = prices[str(limit_time)]

    user = await substract_money(money=user_amount, tg_id=callback.from_user.id)
    
    await buying_mes(payment_amount=true_amount, payment_days=str(limit_time), payment_user_id=user.id)

# result = [200, {
#  "status": "yes",
#  "user_id": "1",
#  "balance": 42.5,
#  "currency": "RUB",
#  "order_id": 12345,
#  "count": 1,
#  "price": 6.3,
#  "period": 7,
#  "country": "ru",
#  "list": {
#    "21": {
#       "id": "21",
#       "ip": "2a00:1838:32:19f:45fb:2640::330",
#       "host": "185.22.134.250",
#       "port": "7330",
#       "user": "5svBNZ",
#       "pass": "iagn2d",
#       "type": "http",
#       "date": "2016-06-19 16:32:39",
#       "date_end": "2012-07-12 11:50:41",
#       "unixtime": 1466379159,
#       "unixtime_end": 1468349441,
#       "active": "1"
#    }
#  }
# }]

async def buying_mes(payment_amount, payment_days, payment_user_id):
    logging.info(payment_days)
    if payment_amount in [110, 400, 680, 900]:
        version = 4
    else:
        version = 3
    result = await buying_proxy.buy_the_proxy(period=int(payment_days))
    logging.info(str(result[0])+'\n'+str(type(result[0])))
    if result[0] == 200:
        resp_buy = result[1]
        proxy_data = {} 
        proxy_data['ipv'] = version
        proxy_data['price_from_proxy'] = resp_buy['price']
        proxy_data['user_id'] = payment_user_id
        proxy_data['country'] = resp_buy["country"]
        for prox in resp_buy['list']:
            for field in resp_buy["list"][prox]:
                proxy_data[field] = resp_buy["list"][prox][field]
        logging.info(proxy_data)
        proxy = await add_new_proxy(proxy_data)
        user = await get_user(user_id=payment_user_id)
        await buying_succes(tg_id=user.tg_id, amount=prices[payment_days], id=proxy_data["id"], proxy_data=proxy)
    else:
        await add_money(user_id=payment_user_id, money=prices[payment_days])
        user = await get_user(user_id=payment_user_id)
        await retutn_money_user(tg_id=user.tg_id, amount=prices[payment_days])

@router.message(F.text == texts.MAIN_BUTTON_1)
async def choose_pc_phone(message: Message):
    add(user_id=message.from_user.id, msg_id=message.message_id)
    await clear(int(message.from_user.id))

    mes = await message.answer("Для какого устройства вам нужен прокси?", reply_markup=keyboards.choose_device)
    add(user_id=message.from_user.id, msg_id=mes.message_id)

@router.callback_query(F.data == texts.MAIN_BUTTON_PC)
async def applicate_prices_pc(callback: CallbackQuery, state: FSMContext):
    await state.set_state(fsm_lists.Buy.limit_time)

    count_of_proxy = await buying_proxy.get_count_of_proxy()
    
    if count_of_proxy < 8:
        await clear(int(callback.from_user.id))
        mes = await callback.message.answer(f"Доступных прокси слишком мало, покупка прокси пока недоступна")
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))
    else:
        await clear(int(callback.from_user.id))
        mes = await callback.message.answer(f"Доступных прокси: {count_of_proxy}")
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))
        mes = await callback.message.answer(texts.PROXY_VIEW_0, reply_markup=keyboards.buy_proxy_pc_0)
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))
        mes = await callback.message.answer(texts.PROXY_VIEW_1, reply_markup=keyboards.buy_proxy_pc_1)
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))
        mes = await callback.message.answer(texts.PROXY_VIEW_2, reply_markup=keyboards.buy_proxy_pc_2)
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))
        mes = await callback.message.answer(texts.PROXY_VIEW_3, reply_markup=keyboards.buy_proxy_pc_3)
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))

@router.callback_query(F.data == texts.MAIN_BUTTON_PHONE)
async def applicate_prices_phone(callback: CallbackQuery, state: FSMContext):
    await state.set_state(fsm_lists.Buy.limit_time)

    count_of_proxy = await buying_proxy.get_count_of_proxy(version=3)
    
    if count_of_proxy < 8:
        await clear(int(callback.from_user.id))
        mes = await callback.message.answer(f"Доступных прокси слишком мало, покупка прокси пока недоступна")
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))
    else:
        await clear(int(callback.from_user.id))
        mes = await callback.message.answer(f"Доступных прокси: {count_of_proxy}")
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))
        mes = await callback.message.answer(texts.PROXY_VIEW_PHONE_0, reply_markup=keyboards.buy_proxy_phone_0)
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))
        mes = await callback.message.answer(texts.PROXY_VIEW_PHONE_1, reply_markup=keyboards.buy_proxy_phone_1)
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))
        mes = await callback.message.answer(texts.PROXY_VIEW_PHONE_2, reply_markup=keyboards.buy_proxy_phone_2)
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))
        mes = await callback.message.answer(texts.PROXY_VIEW_PHONE_3, reply_markup=keyboards.buy_proxy_phone_3)
        add(user_id=int(callback.from_user.id), msg_id=int(mes.message_id))
