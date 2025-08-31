
__all__ = ["router",
           "add",
           "clear"
           ]

from src.handlers.deleting_messages import add, clear
from aiogram import Router
from src.handlers.admin import router as admin_router
from src.handlers.user import router as user_router

router = Router()
router.include_routers(admin_router,
                       user_router)