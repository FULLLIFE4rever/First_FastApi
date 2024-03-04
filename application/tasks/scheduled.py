import smtplib
from tasks.email_temp import create_booking_reminder
from config import settings
from bookings.services import BookingsService
from tasks.celery_conf import celery_worker


@celery_worker.task(name="periodic_task")
def email(days: int):
    bookings = BookingsService.find_need_to_remind(days=days)
    msgs =[]
    for booking in bookings:
        email_to = booking.user.email
        email_to = settings.SMTP_USER
        booking_data = {
            "date_to": booking.date_to,
            "date_from": booking.date_from,
        }
        msg_content = create_booking_reminder(booking_data, email_to, days)
        msgs.append(msg_content)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        for msg_content in msgs:
            server.send_message(msg_content)

