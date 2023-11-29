from django.shortcuts import get_object_or_404

from .models import Item


def add_item(item: dict) -> None:
    Item.objects.create(**item)


def get_item(item_id: int) -> Item:
    return get_object_or_404(Item, pk=item_id)
