from aiogram import Router

from texts import texts
from keyboards import main

from aiogram.types import Message
from aiogram.filters import CommandStart, Command

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(texts.START_MESSAGE, reply_markup=main)
