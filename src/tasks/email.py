import smtplib
from email.message import EmailMessage

from celery import Celery

from ..auth.models import User
from ..config import SMTP_USER, SMTP_PASSWORD

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465


# celery -A src.tasks.tasks:celery worker --loglevel=INFO --pool=solo
# celery -A src.tasks.tasks:celery flower
celery = Celery("tasks", broker="redis://localhost:6379")


def get_email_template_dashboard(message: str, user: User):
    email = EmailMessage()
    email["Subject"] = "Tokens"
    email['From'] = SMTP_USER
    email['To'] = user.email.__str__()

    email.set_content(
        '<div>'
        f'<h1 style="color: red;">Hello, {user.email}😊</h1>'
        f'{message}'
        '</div>',
        subtype='html'
    )
    return email


@celery.task()
def send_email_via_smtp(message: str, user: User):
    email = get_email_template_dashboard(message, user)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(email)
