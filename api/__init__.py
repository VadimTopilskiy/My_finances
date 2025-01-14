from fastapi import APIRouter

from api.handlers import auth_router
from api.login_handler import login_router

routers = APIRouter()
routers.include_router(auth_router, prefix="/auth", tags=["auth"])
routers.include_router(login_router, prefix="/login", tags=["login"])

