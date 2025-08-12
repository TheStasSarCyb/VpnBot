from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

from keyboards import keyboards
from texts import texts
from APIS.proxy import buying_proxy
from APIS.freekassa import generate_new_link

router = Router()

@router.callback_query(F.data[:5] == 'bying')
async def applicate_prices(callback: CallbackQuery):
    count_of_proxy = await buying_proxy.get_count_of_proxy()
    await callback.message.answer(f"Доступных прокси: {count_of_proxy}")
    if callback.data[-1] == '1':
        await callback.answer('Вы выбрали "Купить прокси на 30 дней"')
        await callback.message.answer(f"{texts.CONFIRMATION_PROXY}\n{texts.PROXY_VIEW_1}")
        link = generate_new_link(300)
        await callback.message.answer(f"{texts.PAY_TEXT}\n{link}")
    if callback.data[-1] == '2':
        await callback.answer('Вы выбрали "Купить прокси на 60 дней"')
        await callback.message.answer(f"{texts.CONFIRMATION_PROXY}\n{texts.PROXY_VIEW_2}")
        link = generate_new_link(560)
        await callback.message.answer(f"{texts.PAY_TEXT}\n{link}")
    if callback.data[-1] == '3':
        await callback.answer('Вы выбрали "Купить прокси на 90 дней"')
        await callback.message.answer(f"{texts.CONFIRMATION_PROXY}\n{texts.PROXY_VIEW_3}")
        link = generate_new_link(820)
        await callback.message.answer(f"{texts.PAY_TEXT}\n{link}")

@router.message(F.text == texts.MAIN_BUTTON_1)
async def applicate_prices(message: Message):
    # await message.answer('Показываю цены')
    await message.answer(texts.PROXY_VIEW_1, reply_markup=keyboards.buy_proxy_1)
    await message.answer(texts.PROXY_VIEW_2, reply_markup=keyboards.buy_proxy_2)
    await message.answer(texts.PROXY_VIEW_3, reply_markup=keyboards.buy_proxy_3)