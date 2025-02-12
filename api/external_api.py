from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from schemas.schemas import ConvertedBalances
from service.auth import get_current_user_from_token
from db.models import User
from service.external_api import convert_currency, current_exchange_rate
from service.transaction import _get_current_balance

exchange_router = APIRouter()
websocket_router = APIRouter()


@exchange_router.get("/exchange", response_model=ConvertedBalances)
async def get_current_balance(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
):
    user_id = current_user.id
    balance = await _get_current_balance(user_id, db)
    exchange_rates, eur_to_rub = await current_exchange_rate()
    converted_currency = await convert_currency(balance, exchange_rates, eur_to_rub)
    return {"balances": converted_currency}



