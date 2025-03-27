import stripe

from config.settings import STRIPE_API_KEY
from users.models import SubscriptionToCourse

stripe.api_key = STRIPE_API_KEY


def create_stripe_product(instance):
    """Создаёт продукт в Stripe."""
    product = (
        instance.paid_course if instance.paid_course else instance.paid_lesson
    )
    if not product:
        raise ValueError("Необходимо указать <paid_course> или <paid_lesson>.")
    stripe_product = stripe.Product.create(name=product)
    stripe_product_id = stripe_product.get("id")
    return stripe_product_id


def create_stripe_price(stripe_product_id, amount):
    """Создаёт цену в Stripe."""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product_data={"name": stripe_product_id},
    )
    return price


def create_stripe_session(price):
    """Создаёт сессию в Stripe."""
    session = stripe.checkout.Session.create(
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
        success_url="http://127.0.0.1:8000/",
    )
    return session.get("id"), session.get("url")


def get_data_for_sending_messages(lesson):
    """Получает данные для отправки уведомлений."""
    course = lesson.course
    if course:
        subscriptions = SubscriptionToCourse.objects.filter(course=course.id)
        subscribers_mail = [
            subscriber.user.email for subscriber in subscriptions
        ]
        message = f"В курсе: '{course.name}' обновился урок: '{lesson.name}'."
        subject = "Обновление курса."
        return subscribers_mail, message, subject
