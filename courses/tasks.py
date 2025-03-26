from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER


@shared_task
def send_update_course(subscribers_mail, message, subject):
    """Отправляет уведомление об изменении курса."""
    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=subscribers_mail,
    )
