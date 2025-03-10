from fastapi import APIRouter
from api.category import category_router
from api.external_api import exchange_router, websocket_router
from api.financial_report import report_router
from api.transaction import transaction_router
from api.user import auth_router
from api.auth import login_router

routers = APIRouter()
routers.include_router(auth_router, prefix="/auth", tags=["auth"])
routers.include_router(login_router, prefix="/login", tags=["login"])
routers.include_router(category_router, prefix="/category", tags=["category"])
routers.include_router(transaction_router, prefix="/transaction", tags=["transaction"])
routers.include_router(exchange_router, prefix="/exchange", tags=["exchange"])
routers.include_router(websocket_router, prefix="/ws", tags=["exchange"])
routers.include_router(report_router, prefix="/generate_report", tags=["report"])

