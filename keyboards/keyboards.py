from texts.texts import MAIN_BUTTON_1, MAIN_BUTTON_2, MAIN_BUTTON_3, MAIN_BUTTON_4
from texts import enums

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=MAIN_BUTTON_1), KeyboardButton(text=MAIN_BUTTON_2)], [KeyboardButton(text=MAIN_BUTTON_3), KeyboardButton(text=MAIN_BUTTON_4)]], resize_keyboard=True)

get_prices = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Узнать цены', callback_data='get_prices')]])

buy_proxy_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить прокси на 30 дней', callback_data=enums.Bying_enum.days_30.value)]])
buy_proxy_2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить прокси на 60 дней', callback_data=enums.Bying_enum.days_60.value)]])
buy_proxy_3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить прокси на 90 дней', callback_data=enums.Bying_enum.days_90.value)]])

pay_method_buttons = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="СБП", callback_data=enums.Pay_methods.SBP.value), InlineKeyboardButton(text="На карту", callback_data=enums.Pay_methods.CARD.value)], [InlineKeyboardButton(text="Списать с баланса", callback_data=enums.Pay_methods.ACC.value)]])
pay_prolong_method_buttons = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="СБП", callback_data=enums.Pay_methods.SBPP.value), InlineKeyboardButton(text="На карту", callback_data=enums.Pay_methods.CARDP.value)], [InlineKeyboardButton(text="Списать с баланса", callback_data=enums.Pay_methods.ACCP.value)]])

prolong_buttons = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="10 дней", callback_data='ptolong_time 10'), InlineKeyboardButton(text="30", callback_data='ptolong_time 30')],
                                                         [InlineKeyboardButton(text="60", callback_data='ptolong_time 60'), InlineKeyboardButton(text="90", callback_data='ptolong_time 90')]])

account_money_pay = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='ДА', callback_data='bonuses')]])

account_money_prlolng = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='ДА', callback_data='prolong_bonuses')]])


