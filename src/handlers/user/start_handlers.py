from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from keyboards import keyboards
from texts import texts

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(texts.START_MESSAGE_1, reply_markup=keyboards.main)
    await message.answer(texts.START_MESSAGE_2, reply_markup=keyboards.get_prices)

@router.message(F.text == texts.MAIN_BUTTON_1)
async def user_wants_to_buy(message: Message):
    await message.answer(texts.USER_FIR_BUYING)

@router.message(F.text == texts.MAIN_BUTTON_2)
async def user_wants_to_buy(message: Message):
    await message.answer(texts.USERS_PROXI)

@router.callback_query(F.data == 'get_prices')
async def applicate_prices(callback: CallbackQuery):
    await callback.answer('Показываю цены')
    await callback.message.answer(texts.PROXY_VIEW_1, reply_markup=keyboards.buy_proxy_1)
    await callback.message.answer(texts.PROXY_VIEW_2, reply_markup=keyboards.buy_proxy_2)
    await callback.message.answer(texts.PROXY_VIEW_3, reply_markup=keyboards.buy_proxy_3)