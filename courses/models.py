from django.db import models

blank_null_true = {"blank": True, "null": True}


class Course(models.Model):
    """Описывает учебный курс."""

    name = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(
        verbose_name="Описание курса", **blank_null_true
    )
    picture = models.ImageField(
        upload_to="course/", verbose_name="Изображение", **blank_null_true
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        **blank_null_true,
        verbose_name="Владелец",
        help_text="Укажите владельца курса",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Описывает урок учебного курса."""

    name = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(
        verbose_name="Описание урока", **blank_null_true
    )
    picture = models.ImageField(
        upload_to="lesson/", verbose_name="Изображение", **blank_null_true
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео", **blank_null_true
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        related_name="lessons",
        **blank_null_true,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        **blank_null_true,
        verbose_name="Владелец",
        help_text="Укажите владельца урока",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
