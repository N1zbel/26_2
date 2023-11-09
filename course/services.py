import stripe
from django.conf import settings


def stripe_get_link(obj):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    created_product = stripe.Product.create(name=obj.title)

    created_price = stripe.Price.create(
        unit_amount=obj.price * 100,
        currency="eur",
        product=created_product.id,
    )

    response = stripe.PaymentLink.create(
        line_items=[
            {
                "price": created_price.id,
                "quantity": 1,
            },
        ],
    )
    return response.url