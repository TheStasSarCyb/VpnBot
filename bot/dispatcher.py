from aiogram import Dispatcher
from app.handlers import router

dp = Dispatcher()
dp.include_router(router)