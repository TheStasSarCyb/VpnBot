from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from keyboards import keyboards
from texts import texts

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(texts.START_MESSAGE, reply_markup=keyboards.main)
