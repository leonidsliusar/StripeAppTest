import os
from abc import ABC, abstractmethod
import stripe
from dotenv import load_dotenv

load_dotenv()


class PaymentManager(ABC):
    @abstractmethod
    def get_session(self, item: dict) -> str:
        ...


class StripeManager(PaymentManager):
    _pub_key = os.getenv('STRIPE_PUB_KEY')
    _sec_key = os.getenv('STRIPE_SEC_KEY')
    _success_url = os.getenv('SUCCESS_URL')
    _return_url = os.getenv('RETURN_URL')

    def __init__(self):
        stripe.api_key = self._sec_key
        self._stripe = stripe

    def get_session(self, item: dict) -> str:
        checkout_session = stripe.checkout.Session.create(
            success_url=self._success_url if self._success_url else None,
            cancel_url=self._return_url if self._success_url else None,
            line_items=[
                {
                    "price_data": {
                        "currency": "USD",
                        "product_data": {
                            "name": item.get("name")
                        },
                        "unit_amount": item.get("price"),
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
        )
        return checkout_session.id
