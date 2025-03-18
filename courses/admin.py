from django.contrib import admin

from .models import Course, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_filter = ("name", "owner")


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_filter = ("course", "owner")
