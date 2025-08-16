from aiogram import Router, F
from aiogram.filters import CommandStart, Command, or_f
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from APIS.proxy.buying_proxy import prolong_proxy

router = Router()

@router.callback_query(F.data.startswith('prolong_proxy'))
async def user_prolong_proxy(callback: CallbackQuery):

    calback = callback.data

    proxy_id = str(calback).split()[-1]
    tg_id = callback.from_user.id

    