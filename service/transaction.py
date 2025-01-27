from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from repository.dals import FinancesDAL
from schemas.schemas import TransactionsCreate


async def _add_transactions(user_id: UUID, body: TransactionsCreate,  db: AsyncSession):
    async with db.begin():
        transaction_dal = FinancesDAL(db)
        transactions = await transaction_dal.add_transaction(
            user_id=user_id,
            category_id=body.category_id,
            amount=body.amount,
            type_of_operation=body.type_of_operation)
        return transactions


async def _get_current_balance(user_id: UUID,  db: AsyncSession):
    async with db.begin():
        current_balance_dal = FinancesDAL(db)
        current_balance = await current_balance_dal.get_current_balance(
            user_id=user_id)
        return current_balance

