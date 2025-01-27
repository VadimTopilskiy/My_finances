from fastapi import APIRouter
from api.category import category_router
from api.transaction import transaction_router
from api.user import auth_router
from api.auth import login_router

routers = APIRouter()
routers.include_router(auth_router, prefix="/auth", tags=["auth"])
routers.include_router(login_router, prefix="/login", tags=["login"])
routers.include_router(category_router, prefix="/category", tags=["category"])
routers.include_router(transaction_router, prefix="/transaction", tags=["transaction"])


