from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os


async def generate_pdf_report(user_email: str, transactions: list):
    report_dir = "reports"
    os.makedirs(report_dir, exist_ok=True)
    report_filename = f"report_{user_email.replace('@', '_').replace('.', '_')}_{datetime.now().strftime('%Y%m')}.pdf"
    report_path = os.path.join(report_dir, report_filename)

    c = canvas.Canvas(report_path, pagesize=A4)
    c.setFont("Helvetica", 12)

    c.drawString(200, 800, f"Отчет по транзакциям ({datetime.now().strftime('%B %Y')})")
    c.drawString(200, 780, f"Пользователь: {user_email}")
    c.line(50, 770, 545, 770)

    y_position = 750

    c.drawString(50, y_position, "Дата")
    c.drawString(150, y_position, "Категория")
    c.drawString(300, y_position, "Сумма")
    c.line(50, y_position - 10, 545, y_position - 10)
    y_position -= 20

    for transaction in transactions:
        if y_position < 40:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_position = 800

        c.drawString(50, y_position, transaction.date.strftime('%Y-%m-%d'))
        c.drawString(150, y_position, transaction.categories.name_category)
        c.drawString(300, y_position, f"{transaction.amount:.2f}")
        y_position -= 20

    c.save()
    return report_path
