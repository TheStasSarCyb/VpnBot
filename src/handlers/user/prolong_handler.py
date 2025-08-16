from aiogram import Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from APIS.proxy.buying_proxy import prolong_proxy
from keyboards.keyboards import prolong_buttons

from database.requests_db import get_money, all_users_proxy, get_user, get_proxy
from src.fsm_scripts import fsm_lists, FSMContext


router = Router()

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
    proxy_id = state_data

    print(proxy_id)
    await callback.answer('Сейчас продлим')

    user = await get_user(tg_id=callback.from_user.id)
    user_id = user.id

    proxy = await get_proxy(id_=proxy_id, user_id=user_id)

    days = int(calback.split()[-1])
    if days == 10:
        callback.message.answer("Делаю чек")
    elif days == 30:
        callback.message.answer("Делаю чек")
    elif days == 60:
        callback.message.answer("Делаю чек")    
    elif days == 90:
        callback.message.answer("Делаю чек")

