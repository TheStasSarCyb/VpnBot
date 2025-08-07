from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from keyboards import keyboards
from texts import texts

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(texts.START_MESSAGE, reply_markup=keyboards.main)

@router.message(F.text == texts.MAIN_BUTTON_1)
async def user_wants_to_buy(message: Message):
    await message.answer(texts.USER_FIR_BUYING)

@router.message(F.text == texts.MAIN_BUTTON_2)
async def user_wants_to_buy(message: Message):
    await message.answer(texts.USERS_PROXI)