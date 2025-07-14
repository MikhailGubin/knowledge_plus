import stripe

from config.settings import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY


def create_stripe_product(course):
    """Создает цену в Stripe"""

    product = stripe.Product.create(name=course.name)
    return product.get("id")


def create_stripe_price(amount, course, product_id):
    """Создает цену в Stripe"""

    return stripe.Price.create(
        currency="rub", unit_amount=round(amount * 100), product=product_id
    )


def create_stripe_session(price):
    """Создает сессию в Stripe"""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.id, "quantity": 1}],
        mode="payment",
    )
    return session.get("id"), session.get("url")
