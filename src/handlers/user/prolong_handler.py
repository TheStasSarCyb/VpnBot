from aiogram import Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from APIS.proxy.buying_proxy import prolong_proxy
from keyboards.keyboards import prolong_buttons

from database.requests_db import get_money, all_users_proxy, get_user, get_proxy
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

    await state.set_state(f"prolong_proxy {proxy_id}")

    await callback.answer(f"Вы выбрали прокси id: {proxy_id}")

    await callback.message.answer(f"Выберите время, на которое хотите продлить прокси с id: {proxy_id}", reply_markup=prolong_buttons)

@router.callback_query(F.data.startswith('prolong_time'))
async def user_prolong_proxy(callback: CallbackQuery, state: FSMContext):
    calback = callback.data
    state_data = await state.get_data() # STATE
    # proxy_id = state_data

    # print(proxy_id)
    await callback.answer('Сейчас продлим')

    # user = await get_user(tg_id=callback.from_user.id)
    # user_id = user.id

    # proxy = await get_proxy(id_=proxy_id, user_id=user_id)

    days = int(calback.split()[-1])
    await state.set_state(state_data+' '+days)
    if days == 10:
        callback.message.answer('Вы выбрали "Продлить прокси на 10 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_prolong_method_buttons)
    elif days == 30:
        callback.message.answer('Вы выбрали "Продлить прокси на 30 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_prolong_method_buttons)
    elif days == 60:
        callback.message.answer('Вы выбрали "Продлить прокси на 60 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_prolong_method_buttons)
    elif days == 90:
        callback.message.answer('Вы выбрали "Продлить прокси на 90 дней"\nВыберите метод оплаты:', reply_markup=keyboards.pay_prolong_method_buttons)

@router.callback_query(F.data.in_(["SBPP", "CARDP"]))
async def user_prolong_proxy_payment(callback: CallbackQuery, state: FSMContext):
    meth = str(callback.data)[:-1]

    state_data = await state.get_data() # STATE

    proxy_id = int(str(state_data).split()[-2])
    days = str(state_data).split()[-1]
    amount = prices[days]

    link = generate_new_link(amount=amount, pay_method=meth)

    await callback.message.answer(f"Метод оплаты: {meth}\nК оплате: {amount}RUB\nСсылка для оплаты: {link}\nПосле оплаты ваш прокси будет продлён")


    

    await callback.answer('Оплата')
