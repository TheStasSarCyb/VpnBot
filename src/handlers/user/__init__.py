__all__ = ["router",
           ]

from aiogram import Router
from app.handlers.user.start_handlers import router as start_router
from app.handlers.user.buying_handlers import router as buy_router

router = Router()
router.include_routers(start_router, buy_router
                       )