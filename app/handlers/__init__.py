__all__ = ["router",
           ]

from aiogram import Router
from app.handlers.admin import router as admin_router
from app.handlers.user import router as user_router

router = Router()
router.include_routers(admin_router,
                       user_router)