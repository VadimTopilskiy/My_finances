import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from celery import Celery


app = Celery(
    "service.email_service",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)

app.conf.update(
    result_expires=3600,
)

email_from = os.getenv("EMAIL_FROM")
email_password = os.getenv("EMAIL_PASSWORD")
smtp_server = os.getenv("SMTP_SERVER")
smtp_port = int(os.getenv("SMTP_PORT"))


@app.task
def send_report_email(user_email: str, pdf_content: bytes):
    print("Перешли в метод отправки")
    try:
        print("Начинаем отправку на", user_email)

        msg = MIMEMultipart()
        msg['From'] = 'Acecream0@yandex.ru'
        msg['To'] = user_email
        msg['Subject'] = 'Your Monthly Report'

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(pdf_content)
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename=report.pdf')
        msg.attach(part)

        print("Отправка письма")

        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(email_from, email_password)
        server.sendmail(msg["From"], msg["To"], msg.as_string())
        server.quit()

        print("письмо отправлено")
    except smtplib.SMTPException as e:
        print(f"SMTP error: {e}")
    except Exception as e:
        print(f"Eerror: {e}")
