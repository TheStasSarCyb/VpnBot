__all__ = ["router",
           "retutn_money_user",
           ]

from aiogram import Router
from src.handlers.user.start_handlers import router as start_router
from src.handlers.user.buying_handlers import router as buy_router
from src.handlers.user.prolong_handler import router as prolong_router
from src.handlers.user.users_notify import retutn_money_user

router = Router()

router.include_routers(start_router, buy_router, prolong_router
                       )