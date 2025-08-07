from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from texts import texts
from app.keyboards import main

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(texts.START_MESSAGE, reply_markup=main)
