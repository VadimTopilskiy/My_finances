from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.session import get_db
from schemas.schemas import ReportResponse

from service.financial_report import _generate_report
from uuid import UUID

report_router = APIRouter()


@report_router.post("/", response_model=ReportResponse)
async def generate_report(user_id: UUID, db: AsyncSession = Depends(get_db)):

    return await _generate_report(user_id, db)


# from fastapi import APIRouter
# import aiosmtplib
# from email.mime.text import MIMEText
#
# email_router = APIRouter()
#
# SMTP_HOST = "smtp.yandex.ru"
# SMTP_PORT = 465
# SMTP_USER = "Acecream0@yandex.ru"
# SMTP_PASSWORD = "rnwsbwezywfvsmyd"
#
# @email_router.post("/send-test-email/")
# async def send_test_email():
#     """Отправляет тестовое письмо"""
#     recipient_email = "example@example.com"  # Укажи свою почту для теста
#
#     msg = MIMEText("Hello, this is a test email from FastAPI!", "plain", "utf-8")
#     msg["Subject"] = "Test Email"
#     msg["From"] = SMTP_USER
#     msg["To"] = recipient_email
#
#     try:
#         smtp = aiosmtplib.SMTP(hostname=SMTP_HOST, port=SMTP_PORT, use_tls=True)
#         await smtp.connect()
#         await smtp.login(SMTP_USER, SMTP_PASSWORD)
#         await smtp.send_message(msg)
#         await smtp.quit()
#         return {"message": "Email sent successfully"}
#     except Exception as e:
#         return {"error": str(e)}