__all__ = ["router"]

from aiogram import Router
from app.handlers.admin.start_handlers import router as start_router

router = Router()
router.include_routers(start_router,
                       )