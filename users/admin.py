from django.contrib import admin

from users.models import Payments, SubscriptionToCourse, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ("id", "email", "username")


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ("user", "paid_course", "amount", "created_at")
    list_filter = ("user", "paid_course")


@admin.register(SubscriptionToCourse)
class SubscriptionToCourseAdmin(admin.ModelAdmin):
    list_display = ("user", "course", "start_date")
    list_filter = ("user", "course")


2