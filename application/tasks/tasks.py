import smtplib
from pathlib import Path

from PIL import Image
from pydantic import EmailStr

from config import settings
from tasks.celery_conf import celery_worker
from tasks.email_temp import create_booking_confirmation_template


@celery_worker.task
def process_pic(path: str):
    image_path = Path(path)
    image = Image.open(image_path)
    image_resized = image.resize((160, 100))
    image_resized.save(
        f"frontend/static/images/{image_path.stem}_160_100.webp"
    )


@celery_worker.task
def send_confirm_email(booking: dict, user: EmailStr):
    email = create_booking_confirmation_template(booking, user)
    with smtplib.SMTP_SSL(
        settings.SMTP_HOST, settings.SMTP_PORT
    ) as smtp_server:
        smtp_server.login(settings.SMTP_USER, settings.SMTP_PASS)
        smtp_server.send_message(email)
