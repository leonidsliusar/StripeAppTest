import os
from abc import ABC, abstractmethod
from typing import Union

import stripe
from dotenv import load_dotenv
from overrides import override

from stripeapp.datamodels import DiscountDTO, DiscountDTOUpdate, TaxDTO, TaxDTOUpdate
from stripeapp.models import Discount, Tax
from stripeapp.paymentAPI.exception import PaymentSystemException

load_dotenv()


class PaymentManager(ABC):
    @abstractmethod
    def get_session(self, *args, **kwargs) -> str:
        ...


class ExtendedDiscount(ABC):
    @abstractmethod
    def retrieve_coupon(self, *args, **kwargs):
        ...

    @abstractmethod
    def new_coupon(self, *args, **kwargs):
        ...

    @abstractmethod
    def update_coupon(self, *args, **kwargs):
        ...

    @abstractmethod
    def delete_coupon(self, *args, **kwargs):
        ...


class ExtendedTax(ABC):
    @abstractmethod
    def retrieve_tax(self, *args, **kwargs):
        ...

    @abstractmethod
    def new_tax(self, *args, **kwargs):
        ...

    @abstractmethod
    def update_tax(self, *args, **kwargs):
        ...

    @abstractmethod
    def delete_tax(self, *args, **kwargs):
        ...


class StripeManager(PaymentManager):
    _pub_key = os.getenv("STRIPE_PUB_KEY")
    _sec_key = os.getenv("STRIPE_SEC_KEY")
    _success_url = os.getenv("SUCCESS_URL")
    _return_url = os.getenv("RETURN_URL")

    def __init__(self):
        stripe.api_key = self._sec_key
        self._stripe = stripe

    def get_session(self, item: dict, *args, **kwargs) -> str:
        checkout_session = stripe.checkout.Session.create(
            success_url=self._success_url+f'item/{item.get("id")}' if self._success_url else None,
            cancel_url=self._return_url+f'item/{item.get("id")}' if self._success_url else None,
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item.get("name")},
                        "unit_amount": item.get("price"),
                    },
                    "quantity": 1,
                },
            ],
            mode="payment",
        )
        return checkout_session.id


class StripeManagerExtend(StripeManager, ExtendedTax, ExtendedDiscount):
    @override
    def get_session(self, order: dict, *args, **kwargs) -> str:
        checkout_session = stripe.checkout.Session.create(
            success_url=self._success_url+f'order/{order.get("id")}' if self._success_url else None,
            cancel_url=self._return_url+f'order/{order.get("id")}' if self._success_url else None,
            line_items=self._get_line_items(order),
            mode="payment",
            discounts=[{"coupon": order.get("discount").get("id")}],
        )
        return checkout_session.id

    def _get_line_items(self, order: dict) -> list:
        line_items = []
        for item in order.get("items"):
            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": item.get("name")},
                        "unit_amount": item.get("price"),
                    },
                    "quantity": 1,
                    "tax_rates": [order.get("tax").get("id")],
                }
            )
        return line_items

    def retrieve_coupon(self, instance_id: Union[str, int], *args, **kwargs) -> dict:
        try:
            discount = self._stripe.Coupon.retrieve(str(instance_id))
            discount_dto = DiscountDTO.model_validate(discount).model_dump(
                exclude_none=True
            )
            return discount_dto
        except Exception as e:
            raise PaymentSystemException(str(e))

    def new_coupon(self, instance: Discount, *args, **kwargs) -> dict:
        try:
            dto_discount = DiscountDTO.model_validate(instance.__dict__).model_dump(
                exclude_none=True
            )
            coupon = self._stripe.Coupon.create(**dto_discount)
            return coupon
        except Exception as e:
            raise PaymentSystemException(str(e))

    def update_coupon(self, instance: Discount, *args, **kwargs) -> None:
        """Updates the metadata of a coupon.
        Other coupon details (currency, duration, amount_off) are, by design, not editable.

        As I found out name could be changed to
        """
        try:
            dto_discount = DiscountDTOUpdate.model_validate(
                instance.__dict__
            ).model_dump(exclude_none=True)
            self._stripe.Coupon.modify(**dto_discount)
        except Exception as e:
            raise PaymentSystemException(str(e))

    def delete_coupon(self, coupon_id: Union[str, int], *args, **kwargs) -> None:
        try:
            self._stripe.Coupon.delete(str(coupon_id))
        except Exception as e:
            raise PaymentSystemException(str(e))

    def retrieve_tax(self, instance_id: Union[str, int], *args, **kwargs) -> dict:
        try:
            tax = self._stripe.TaxRate.retrieve(str(instance_id))
            return TaxDTO.model_validate(tax).model_dump(exclude_none=True)
        except Exception as e:
            raise PaymentSystemException(str(e))

    def new_tax(self, instance: Tax, *args, **kwargs) -> dict:
        try:
            dto_tax = TaxDTO.model_validate(instance.__dict__).model_dump(
                exclude_none=True, exclude={"id", "pk"}
            )
            return self._stripe.TaxRate.create(**dto_tax)
        except Exception as e:
            raise PaymentSystemException(str(e))

    def update_tax(self, instance: Tax, tax_id: str, *args, **kwargs):
        try:
            dto_tax = TaxDTOUpdate.model_validate(instance.__dict__).model_dump(
                exclude_none=True
            )
            self._stripe.TaxRate.modify(id=str(tax_id), **dto_tax)
        except Exception as e:
            raise PaymentSystemException(str(e))

    def delete_tax(self, tax_id: str, *args, **kwargs):
        try:
            self._stripe.TaxRate.modify(id=str(tax_id), active=False)
        except Exception as e:
            raise PaymentSystemException(str(e))
