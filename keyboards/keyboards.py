from texts.texts import MAIN_BUTTON_1, MAIN_BUTTON_2

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=MAIN_BUTTON_1), KeyboardButton(text=MAIN_BUTTON_2)]])

get_prices = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Узнать цены', callback_data='get_prices')]])