from aiogram import Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards import keyboards
from texts import texts
from APIS.proxy import buying_proxy
from src.fsm_scripts import fsm_lists, FSMContext

from database.requests_db import get_money, all_users_proxy
from src.handlers.deleting_messages import add, clear

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    add(user_id=message.from_user.id, msg_id=message.message_id)
    await clear(int(message.from_user.id))
    mes = await message.answer(texts.START_MESSAGE_1, reply_markup=keyboards.main)
    add(user_id=int(message.from_user.id), msg_id=mes.message_id )
    mes = await message.answer(texts.START_MESSAGE_2, reply_markup=keyboards.get_prices)
    add(user_id=int(message.from_user.id), msg_id=mes.message_id )

@router.message(or_f(F.text == texts.MAIN_BUTTON_2, Command("profile")))
async def users_proxy(message: Message):


    tg_id = message.from_user.id
    add(user_id=tg_id, msg_id=message.message_id)
    username = message.from_user.username

    money = await get_money(tg_id=tg_id, username=username)
    proxies = await all_users_proxy(tg_id=tg_id, username=username)
    
    await clear(int(message.from_user.id))
    
    mes =await message.answer(texts.PROFILE_INFO(money))
    add(user_id=int(message.from_user.id), msg_id=mes.message_id)


    
    for proxy in proxies:
        str_proxies = "<b>id прокси: </b>" + str(proxy.id_)+'\n'
        str_proxies += '<b>ip: </b>' + str(proxy.ip) + '\n'
        str_proxies += '<b>port: </b>' + str(proxy.port) + '\n'
        str_proxies += '<b>логин: </b>' + str(proxy.user_auth) + '\n'
        str_proxies += '<b>пароль: </b>' + str(proxy.password) + '\n'
        str_proxies += '<b>дата начала прокси: </b>' + str(proxy.date) + '\n'
        str_proxies += '<b>дата истечения прокси: </b>' + str(proxy.date_end) + '\n'
        str_proxies += '<b>протокол: </b>' + str(proxy.protocol) +'\n'
        mes = await message.answer(str_proxies, reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=f"Продлить прокси с id {proxy.id_}", callback_data='prolong_proxy '+str(proxy.id_))]]), parse_mode='HTML')
        add(user_id=int(message.from_user.id), msg_id=mes.message_id)


@router.message(F.text == texts.MAIN_BUTTON_3)
async def instruction(message: Message):
    add(user_id=message.from_user.id, msg_id=message.message_id)
    await clear(int(message.from_user.id))
    mes = await message.answer(texts.INSTRUCTION)
    add(user_id=int(message.from_user.id), msg_id=mes.message_id)

@router.message(F.text == texts.MAIN_BUTTON_4)
async def support(message: Message):
    add(user_id=message.from_user.id, msg_id=message.message_id)
    await clear(int(message.from_user.id))
    mes = await message.answer(texts.SUPPORT)
    add(user_id=int(message.from_user.id), msg_id=mes.message_id)


@router.callback_query(F.data == 'get_prices')
async def applicate_prices(callback: CallbackQuery, state: FSMContext):
    await state.set_state(fsm_lists.Buy.limit_time)

    count_of_proxy = await buying_proxy.get_count_of_proxy()

    await callback.answer('Показываю цены')
    await clear(int(callback.from_user.id))
    
    if count_of_proxy < 8:
        mes = await callback.message.answer(texts.PROXY_VIEW_1)
        add(user_id=int(callback.from_user.id), msg_id=mes.message_id )

        mes = await callback.message.answer(texts.PROXY_VIEW_2)
        add(user_id=int(callback.from_user.id), msg_id=mes.message_id )

        mes = await callback.message.answer(texts.PROXY_VIEW_3)
        add(user_id=int(callback.from_user.id), msg_id=mes.message_id )

        mes = await callback.message.answer(f"Доступных прокси слишком мало, вы пока не можете покупка прокси пока недоступна")
        add(user_id=int(callback.from_user.id), msg_id=mes.message_id )

    else:
        mes = await callback.message.answer(f"Доступных прокси: {count_of_proxy}")
        add(user_id=int(callback.from_user.id), msg_id=mes.message_id )

        mes = await callback.message.answer(texts.PROXY_VIEW_1, reply_markup=keyboards.buy_proxy_1)
        add(user_id=int(callback.from_user.id), msg_id=mes.message_id )

        mes = await callback.message.answer(texts.PROXY_VIEW_2, reply_markup=keyboards.buy_proxy_2)
        add(user_id=int(callback.from_user.id), msg_id=mes.message_id )

        mes = await callback.message.answer(texts.PROXY_VIEW_3, reply_markup=keyboards.buy_proxy_3)
        add(user_id=int(callback.from_user.id), msg_id=mes.message_id )
