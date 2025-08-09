from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from keyboards import keyboards
from texts import texts

router = Router()

@router.callback_query(F.data[:5] == 'bying')
async def applicate_prices(callback: CallbackQuery):
    if callback.data[-1] == '1':
        await callback.answer('Вы выбрали "Купить прокси на 30 дней"')
    if callback.data[-1] == '2':
        await callback.answer('Вы выбрали "Купить прокси на 60 дней"')
    if callback.data[-1] == '3':
        await callback.answer('Вы выбрали "Купить прокси на 90 дней"')

@router.message(F.text == texts.MAIN_BUTTON_1)
async def applicate_prices(message: Message):
    # await message.answer('Показываю цены')
    await message.answer(texts.PROXY_VIEW_1, reply_markup=keyboards.buy_proxy_1)
    await message.answer(texts.PROXY_VIEW_2, reply_markup=keyboards.buy_proxy_2)
    await message.answer(texts.PROXY_VIEW_3, reply_markup=keyboards.buy_proxy_3)