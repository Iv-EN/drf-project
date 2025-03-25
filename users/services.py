import stripe

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def create_stripe_price(amount):
    """Создаёт цену в Stripe."""
    price = stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product_data={"name": "Платёж"},
    )
    return price


def create_stripe_session(price):
    """Создаёт сессию в Stripe."""
    session = stripe.checkout.Session.create(
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
        success_url="http://127.0.0.1:8000",
    )
    return session.get("id"), session.get("url")
