__all__ = ["router",
           ]

from aiogram import Router
from src.handlers.user.start_handlers import router as start_router
from src.handlers.user.buying_handlers import router as buy_router

router = Router()
router.include_routers(start_router, buy_router
                       )