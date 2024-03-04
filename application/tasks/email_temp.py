from email.message import EmailMessage

from pydantic import EmailStr

from config import settings


def create_booking_confirmation_template(booking: dict, user: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Подтверждение боронирования"
    email["From"] = settings.SMTP_USER
    email["To"] = settings.SMTP_USER
    email.set_content(
        f"""<h1>Подтвердите бронирование</h1>
        Вы забронировали отель
         с {booking['date_from']} по {booking['date_to']}""",
        subtype="html",
    )
    return email

def create_booking_reminder(booking: dict, user: EmailStr):
    email = EmailMessage()
    email["Subject"] = "Напоминание о боронировании"
    email["From"] = settings.SMTP_USER
    email["To"] = user
    email.set_content(
        f"""<h1>Напоминание о бронировании</h1>
        Вы забронировали отель на {booking['date_to']-booking['date_from']-1}
         с {booking['date_from']} по {booking['date_to']}""",
        subtype="html",
    )
    return email
