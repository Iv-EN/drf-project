from users.models import SubscriptionToCourse


def get_data_for_sending_messages(lesson, change):
    """Получает данные для отправки уведомлений."""
    course = lesson.course
    if course:
        subscriptions = SubscriptionToCourse.objects.filter(course=course.id)
        subscribers_mail = [
            subscriber.user.email for subscriber in subscriptions
        ]
        if change == "created":
            message = f"В курсе: '{course.name}' новый урок - '{lesson.name}'."
        elif change == "updated":
            message = (
                f"В курсе: '{course.name}' изменен урок - '{lesson.name}'."
            )
        elif change == "deleted":
            message = (
                f"Из курса: '{course.name}' удален урок - '{lesson.name}'."
            )
        else:
            message = f"В курсе: '{course.name}' произошли изменения."
        subject = "Обновление курса."
        return subscribers_mail, message, subject
