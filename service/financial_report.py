from datetime import datetime, timedelta, timezone
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from repository.dals import UserDAL, FinancesDAL
from service.pdf_generator import generate_pdf_report
from service.email_service import send_report_email


async def _generate_report(user_id: UUID, db: AsyncSession):
    now = datetime.now(timezone.utc)
    current_year = now.year
    current_month = now.month

    async with db.begin():
        user_dal = UserDAL(db)
        current_user = await user_dal.get_user_by_id(user_id)
        if not current_user:
            return {"error": "User not found"}

        finances_dal = FinancesDAL(db)
        transaction_for_last_month = await finances_dal.get_transactions_for_month(
            user_id,
            year=current_year,
            month=current_month)

    if not transaction_for_last_month:
        return {"error": "No transactions found for the last month"}

    report_path = await generate_pdf_report(current_user.email, transaction_for_last_month)

    print("Отправка отчета через Celery-задачу")
    with open(report_path, "rb") as f:
        pdf_content = f.read()

    send_report_email.delay(current_user.email, pdf_content)
    #send_report_email(current_user.email, pdf_content)

    return {"message": "Report generation started, email will be sent"}
