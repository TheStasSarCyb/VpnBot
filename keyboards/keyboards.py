from texts.texts import MAIN_BUTTON_1, MAIN_BUTTON_2, MAIN_BUTTON_3, MAIN_BUTTON_4
from texts import enums

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=MAIN_BUTTON_1), KeyboardButton(text=MAIN_BUTTON_2)], [KeyboardButton(text=MAIN_BUTTON_3), KeyboardButton(text=MAIN_BUTTON_4)]], resize_keyboard=True, one_time_keyboard=False)

get_prices = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Узнать цены', callback_data='get_prices')]])

buy_proxy_pc_0 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить прокси на 7 дней', callback_data=enums.Bying_enum.days_pc_7.value)]])
buy_proxy_pc_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить прокси на 30 дней', callback_data=enums.Bying_enum.days_pc_30.value)]])
buy_proxy_pc_2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить прокси на 60 дней', callback_data=enums.Bying_enum.days_pc_60.value)]])
buy_proxy_pc_3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить прокси на 90 дней', callback_data=enums.Bying_enum.days_pc_90.value)]])

buy_proxy_phone_0 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить прокси на 7 дней', callback_data=enums.Bying_enum.days_phone_7.value)]])
buy_proxy_phone_1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить прокси на 30 дней', callback_data=enums.Bying_enum.days_phone_30.value)]])
buy_proxy_phone_2 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить прокси на 60 дней', callback_data=enums.Bying_enum.days_phone_60.value)]])
buy_proxy_phone_3 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Купить прокси на 90 дней', callback_data=enums.Bying_enum.days_phone_90.value)]])

pay_method_buttons = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="СБП", callback_data=enums.Pay_methods.SBP.value), InlineKeyboardButton(text="На карту", callback_data=enums.Pay_methods.CARD.value)], [InlineKeyboardButton(text="Списать с баланса", callback_data=enums.Pay_methods.ACC.value)]])
pay_prolong_method_buttons = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="СБП", callback_data=enums.Pay_methods.SBPP.value), InlineKeyboardButton(text="На карту", callback_data=enums.Pay_methods.CARDP.value)], [InlineKeyboardButton(text="Списать с баланса", callback_data=enums.Pay_methods.ACCP.value)]])

prolong_buttons = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="7 дней", callback_data='ptolong_time 7'), InlineKeyboardButton(text="30 дней", callback_data='ptolong_time 30')],
                                                         [InlineKeyboardButton(text="60 дней", callback_data='ptolong_time 60'), InlineKeyboardButton(text="90 дней", callback_data='ptolong_time 90')]])

choose_device = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='ПК', callback_data='PC'), InlineKeyboardButton(text='Телефон', callback_data='Phone')]])

account_money_pay = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='ДА', callback_data='bonuses')]])

account_money_prlolng = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='ДА', callback_data='prolong_bonuses')]])

choose_instruction = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="ПК"), KeyboardButton(text="Айфон")], [KeyboardButton(text="Андроид")]], resize_keyboard=True, one_time_keyboard=False)
