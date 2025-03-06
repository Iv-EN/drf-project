from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Описывает пользователя."""

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    phone_number = models.CharField(
        max_length=15, blank=True, null=True, verbose_name="Номер телефона"
    )
    avatar = models.ImageField(
        upload_to="users/avatars", blank=True, null=True, verbose_name="Фото"
    )
    city = models.CharField(
        max_length=25, blank=True, null=True, verbose_name="Город"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
