from fastapi import APIRouter

from api.handlers import auth_router, new_router

routers = APIRouter()
routers.include_router(auth_router, prefix="/auth", tags=["auth"])
routers.include_router(new_router)
