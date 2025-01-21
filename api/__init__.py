from fastapi import APIRouter

from api.category_handler import category_router
from api.user_handlers import auth_router
from api.login_handler import login_router

routers = APIRouter()
routers.include_router(auth_router, prefix="/auth", tags=["auth"])
routers.include_router(login_router, prefix="/login", tags=["login"])
routers.include_router(category_router, prefix="/category", tags=["category"])

