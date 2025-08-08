__all__ = ["router",
           ]

from aiogram import Router
from src.handlers.admin import router as admin_router
from src.handlers.user import router as user_router

router = Router()
router.include_routers(admin_router,
                       user_router)