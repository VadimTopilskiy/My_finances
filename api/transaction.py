from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from service.auth import get_current_user_from_token
from service.transaction import _add_transactions, _get_current_balance
from db.models import User
from db.session import get_db
from schemas.schemas import TransactionsCreate, CurrentBalanceResponse

transaction_router = APIRouter()


@transaction_router.post("/transactions", response_model=TransactionsCreate)
async def add_transactions(
        body: TransactionsCreate,
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)):
    user_id = current_user.id
    transaction = await _add_transactions(user_id, body, db)
    return transaction


@transaction_router.get("/transactions", response_model=CurrentBalanceResponse)
async def get_current_balance(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token)):
    user_id = current_user.id
    transaction = await _get_current_balance(user_id, db)
    return CurrentBalanceResponse(current_balance=transaction)
