# Generated by Django 5.1.6 on 2025-03-05 20:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("courses", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="course",
            name="description",
            field=models.TextField(
                blank=True, null=True, verbose_name="Описание курса"
            ),
        ),
        migrations.AlterField(
            model_name="course",
            name="picture",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="course/",
                verbose_name="Изображение",
            ),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="course",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="lessons",
                to="courses.course",
                verbose_name="Курс",
            ),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="description",
            field=models.TextField(
                blank=True, null=True, verbose_name="Описание урока"
            ),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="picture",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="lesson/",
                verbose_name="Изображение",
            ),
        ),
        migrations.AlterField(
            model_name="lesson",
            name="video_url",
            field=models.URLField(
                blank=True, null=True, verbose_name="Ссылка на видео"
            ),
        ),
    ]
