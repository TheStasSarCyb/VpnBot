from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from texts import MAIN_BUTTON_1, MAIN_BUTTON_2

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text=MAIN_BUTTON_1), KeyboardButton(text=MAIN_BUTTON_2)], []])