from typing import Optional, Union
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from .models import Item, Discount, Tax, Order


def echo(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(result.query)
        return result.first()

    return wrapper


def add_item(item: dict) -> None:
    Item.objects.create(**item)


def get_item(item_id: int) -> Item:
    return get_object_or_404(Item, pk=item_id)


def get_order(order_id: Union[int, str]) -> Optional[Order]:
    return (
        Order.objects.prefetch_related("items")
        .select_related("discount")
        .select_related("tax")
        .filter(pk=order_id)
        .first()
    )


def get_orders_by_item(item_id: Union[int, str]) -> list[Order]:
    response = (
        Order.objects.filter(items__pk=item_id)
        .select_related("discount")
        .select_related("tax")
        .prefetch_related("items")
        .all()
    )
    return list(response)
