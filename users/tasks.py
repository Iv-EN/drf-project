from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from .models import User


@shared_task
def blocking_user():
    """Блокирует пользователя, если он не заходил более месяца."""
    users = User.objects.filter(last_login__isnull=False)
    for user in users:
        if (user.last_login + timedelta(days=30)) < timezone.now() and (
            user.is_active
        ):
            user.is_active = False
            user.save()
            print(f"Пользователь {user.username} <{user.email}> заблокирован")
