from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Lesson

blank_null_true = {"blank": True, "null": True}


class User(AbstractUser):
    """Описывает пользователя."""

    email = models.EmailField(unique=True, verbose_name="Электронная почта")
    phone_number = models.CharField(
        max_length=15, **blank_null_true, verbose_name="Номер телефона"
    )
    avatar = models.ImageField(
        upload_to="users/avatars", **blank_null_true, verbose_name="Фото"
    )
    city = models.CharField(
        max_length=25, **blank_null_true, verbose_name="Город"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payments(models.Model):
    """Описывает платежи пользователей."""

    class Way(models.TextChoices):
        CASH = "cash", "Наличные"
        BANK_TRANSFER = "bank_transfer", "Банковский перевод"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="payments",
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Сумма оплаты"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата оплаты"
    )
    paid_lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
        **blank_null_true,
    )
    paid_course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
        **blank_null_true,
    )
    payment_method = models.CharField(
        max_length=20,
        choices=Way.choices,
        verbose_name="Способ оплаты",
    )
    session_id = models.CharField(
        max_length=255,
        **blank_null_true,
        verbose_name="ID сессии",
    )
    link = models.URLField(
        max_length=400,
        **blank_null_true,
        verbose_name="Ссылка на оплату",
    )
    status = models.CharField(
        max_length=20, **blank_null_true, verbose_name="Статус оплаты"
    )

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.paid_course if self.paid_course else self.paid_lesson}"


class SubscriptionToCourse(models.Model):
    """Описывает подписки пользователей на курсы."""

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс"
    )
    start_date = models.DateField(
        auto_now_add=True, verbose_name="Дата начала подписки"
    )

    def __str__(self):
        return f"{self.user} - {self.course}"

    class Meta:
        verbose_name = "Подписка на курс"
        verbose_name_plural = "Подписки на курсы"
        unique_together = ("user", "course")
        ordering = ["-start_date", "user", "course"]
