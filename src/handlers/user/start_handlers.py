from aiogram import Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message, CallbackQuery

from keyboards import keyboards
from texts import texts
from APIS.proxy import buying_proxy
from src.fsm_scripts import fsm_lists, FSMContext

from database.requests_db import get_money

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(texts.START_MESSAGE_1, reply_markup=keyboards.main)
    await message.answer(texts.START_MESSAGE_2, reply_markup=keyboards.get_prices)

@router.message(or_f(F.text == texts.MAIN_BUTTON_2, Command("profile")))
async def users_proxy(message: Message):
    tg_id = message.from_user.id
    username = message.from_user.username

    money = await get_money(tg_id=tg_id, username=username)
    await message.answer(texts.PROFILE_INFO(money))

@router.message(F.text == texts.MAIN_BUTTON_3)
async def instruction(message: Message):
    await message.answer(texts.INSTRUCTION)

@router.message(F.text == texts.MAIN_BUTTON_4)
async def support(message: Message):
    await message.answer(texts.SUPPORT)

@router.callback_query(F.data == 'get_prices')
async def applicate_prices(callback: CallbackQuery, state: FSMContext):
    await state.set_state(fsm_lists.Buy.limit_time)

    count_of_proxy = await buying_proxy.get_count_of_proxy()

    await callback.answer('Показываю цены')
    
    if count_of_proxy < 8:
        await callback.message.answer(texts.PROXY_VIEW_1)
        await callback.message.answer(texts.PROXY_VIEW_2)
        await callback.message.answer(texts.PROXY_VIEW_3)
        await callback.message.answer(f"Доступных прокси слишком мало, вы пока не можете покупка прокси пока недоступна")
    else:
        await callback.message.answer(f"Доступных прокси: {count_of_proxy}")
        await callback.message.answer(texts.PROXY_VIEW_1, reply_markup=keyboards.buy_proxy_1)
        await callback.message.answer(texts.PROXY_VIEW_2, reply_markup=keyboards.buy_proxy_2)
        await callback.message.answer(texts.PROXY_VIEW_3, reply_markup=keyboards.buy_proxy_3)