from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from keyboards import keyboards
from texts import texts
from texts import enums
from APIS.proxy import buying_proxy
from APIS.freekassa import generate_new_link
from src.fsm_scripts import fsm_lists, FSMContext
from database import User, Pay, Proxy, async_session, add_user_and_pay
from sqlalchemy import select, update, delete, func
router = Router()

amounts = [300, 560, 820]

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

@router.callback_query(fsm_lists.Buy.pay_method, F.data.in_(["SBP", "CARD"]))
async def pay_method_handler(callback: CallbackQuery, state: FSMContext):
    data = callback.data # CALLBACK
    state_data = await state.get_data() # STATE
    limit_time = state_data['limit_time'] # STATE

    amount = amounts[limit_time//30-1]

    await callback.answer(f"Метод оплаты выбран")
    if data == enums.Pay_methods.SBP.value:
        link = generate_new_link(amount=limit_time, pay_method=enums.Pay_methods.SBP.value)
        await callback.message.answer(f"Метод оплаты: {enums.Pay_methods.SBP.value}\nК оплате: {amount}RUB\nСсылка для оплаты: {link}\nПосле оплаты, вы получите ip и логин для подключения прокси сервера")

    elif data == enums.Pay_methods.CARD.value:
        link = generate_new_link(amount=limit_time, pay_method=enums.Pay_methods.CARD.value)
        await callback.message.answer(f"Метод оплаты: {enums.Pay_methods.CARD.value}\nК оплате: {amount}RUB\nСсылка для оплаты: {link}\nПосле оплаты, вы получите ip и логин для подключения прокси сервера")

    await add_user_and_pay(tg_id=callback.from_user.id, id=link.split('/')[-2], amount=amount, username=callback.from_user.full_name)
    

@router.message(F.text == texts.MAIN_BUTTON_1)
async def applicate_prices(message: Message, state: FSMContext):
    await state.set_state(fsm_lists.Buy.limit_time)

    count_of_proxy = await buying_proxy.get_count_of_proxy()

    await message.answer(f"Доступных прокси: {count_of_proxy}")

    await message.answer(texts.PROXY_VIEW_1, reply_markup=keyboards.buy_proxy_1)
    await message.answer(texts.PROXY_VIEW_2, reply_markup=keyboards.buy_proxy_2)
    await message.answer(texts.PROXY_VIEW_3, reply_markup=keyboards.buy_proxy_3)