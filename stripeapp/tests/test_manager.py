from datetime import datetime, timezone
from typing import Optional
import pytest
from stripeapp.datamodels import DiscountDTO, TaxDTO, OrderDTO
from stripeapp.models import Discount, Tax, Item, Order
from stripeapp.paymentAPI.exception import PaymentSystemException
from stripeapp.paymentAPI.manager import StripeManagerExtend

s = StripeManagerExtend()


def serialize_discount(model_instance: Discount):
    return DiscountDTO.model_validate(model_instance.__dict__).model_dump(
        exclude_none=True
    )


def serialize_tax(model_instance: Tax, tax_id: Optional[str] = None):
    if tax_id:
        model_instance.pk = tax_id
    return TaxDTO.model_validate(model_instance.__dict__).model_dump(exclude_none=True)


@pytest.mark.parametrize("mock_data", (Discount,), indirect=True)
def test_stripe_api_coupon(mock_data):
    try:
        s.delete_coupon(1)
    except PaymentSystemException:
        ...
    model_instance = Discount(**mock_data)
    s.new_coupon(model_instance)
    assert s.retrieve_coupon(1) == serialize_discount(model_instance)
    model_instance.name = "fo_2"
    s.update_coupon(model_instance)
    assert s.retrieve_coupon(1) == serialize_discount(model_instance)
    s.delete_coupon(1)
