from aiogram import Dispatcher
from src.handlers import router

dp = Dispatcher()
dp.include_router(router)