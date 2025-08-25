from aiogram import Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from APIS.proxy import buying_proxy
from keyboards.keyboards import prolong_buttons

from database.requests_db import get_money, all_users_proxy, get_user, get_proxy, add_prolong_pay, substract_money, prolong_proxy_db, add_money
from src.handlers.user.users_notify import retutn_money_user, buying_succes, prolong_succes
from src.fsm_scripts import fsm_lists, FSMContext
from APIS.freekassa import generate_new_link
from keyboards import keyboards


router = Router()

prices = {
    "10": 100,
    "30": 300,
    "60": 560,
    "90": 820
}

@router.callback_query(F.data.startswith('prolong_proxy'))
async def user_wants_prolong(callback: CallbackQuery, state: FSMContext):
    calback = callback.data
    proxy_id = str(calback).split()[-1]


    await state.update_data(proxy_id=proxy_id)

    await state.set_state("prolong_waiting_duration")

    await callback.answer(f"Вы выбрали прокси id: {proxy_id}")

    await callback.message.answer(f"Выберите время, на которое хотите продлить прокси с id: {proxy_id}", reply_markup=prolong_buttons)

@router.callback_query(F.data.startswith('ptolong_time'))
async def user_prolong_proxy(callback: CallbackQuery, state: FSMContext):
    calback = callback.data
    data = await state.get_data()
    proxy_id = data.get("proxy_id")

    # print(proxy_id)
    await callback.answer('Сейчас продлим')

    # user = await get_user(tg_id=callback.from_user.id)
    # user_id = user.id

    # proxy = await get_proxy(id_=proxy_id, user_id=user_id)

    days = int(calback.split()[-1])
    await state.update_data(proxy_id=proxy_id, days=days)

    await state.set_state("prolong_waiting_duration")
    if days == 10:
        await state.update_data(limit_time=10) # STATE
        await callback.message.answer('Вы выбрали "Продлить прокси на 10 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_prolong_method_buttons)
    elif days == 30:
        await state.update_data(limit_time=30) # STATE
        await callback.message.answer('Вы выбрали "Продлить прокси на 30 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_prolong_method_buttons)
    elif days == 60:
        await state.update_data(limit_time=60) # STATE
        await callback.message.answer('Вы выбрали "Продлить прокси на 60 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_prolong_method_buttons)
    elif days == 90:
        await state.update_data(limit_time=90) # STATE
        await callback.message.answer('Вы выбрали "Продлить прокси на 90 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_prolong_method_buttons)

@router.callback_query(F.data.in_(["SBPP", "CARDP"]))
async def user_prolong_proxy_payment(callback: CallbackQuery, state: FSMContext):
    meth = str(callback.data)[:-1]
    state_data = await state.get_data() # STATE

    proxy_id = int(state_data.get("proxy_id"))
    days = state_data.get("days")
    print(days)
    amount = prices[str(days)]

    link = generate_new_link(amount=amount, pay_method=meth)

    await callback.message.answer(f"Метод оплаты: {meth}\nК оплате: {amount}RUB\nСсылка для оплаты: {link}\nПосле оплаты ваш прокси будет продлён")

    await add_prolong_pay(tg_id=callback.from_user.id, id=link.split('/')[-2], amount=amount, username=callback.from_user.full_name, typ="prolong", id_=proxy_id)

    await callback.answer('Оплата')

@router.callback_query(F.data.in_(["ACCP"]))
async def prolong_proxy_acc(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data() # STATE

    proxy_id = int(state_data.get("proxy_id"))
    days = state_data.get("days")
    print(days)
    amount = prices[str(days)]

    await callback.answer("Метод оплаты выбран")
    user = await get_user(tg_id=callback.from_user.id)
    if user.money >= amount:
        await callback.message.answer(f"У вас {user.money}RUB\nМожно оплатить прокси, списав с баланса\nСписать {amount}RUB?", reply_markup=keyboards.account_money_prlolng)

@router.callback_query(F.data.startswith('prolong_bonuses'))
async def acc_payment(callback: CallbackQuery, state: FSMContext):
    await callback.answer("Оплата прошла")

    state_data = await state.get_data() # STATE
    limit_time = state_data['limit_time'] # STATE

    amount = prices[str(limit_time)]

    user = await substract_money(money=amount, tg_id=callback.from_user.id)
    
    await prolong_mes(payment_amount=amount, payment_days=limit_time, payment_user_id=user.id)

async def prolong_mes(payment_days, payment_user_id, payment_amount):
    result = await buying_proxy.prolong_proxy(payment_days)
    if result[0] == '200':
        proxy_data = {} 
        resp_prolong = result[1]
        for prox in resp_prolong['list']:
            proxy_data['id'] = prox
            for field in resp_prolong["list"][prox]:
                proxy_data[field] = resp_prolong["list"][prox][field]
        print(proxy_data)
        await prolong_proxy_db(proxy_data['id'], proxy_data['date_end'])
        user = await get_user(user_id=payment_user_id)
        await prolong_succes(tg_id=user.tg_id, amount=payment_amount, id=proxy_data["id"])
    else:
        await add_money(user_id=payment_user_id, money=payment_amount)
        user = await get_user(user_id=payment_user_id)
        await retutn_money_user(tg_id=user.tg_id, amount=payment_amount)
