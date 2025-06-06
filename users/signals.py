from django.contrib.auth import user_logged_in
from django.dispatch import receiver
from django.utils import timezone


@receiver(user_logged_in)
def update_last_login(sender, request, user, **kwargs):
    """Обновляет поле last_login у модели User."""
    user.last_login = timezone.now()
    user.save()
