import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from stripeapp.services import ItemService, buy_services, BuyServices, OrderService


class ItemView(View):
    def get(self, request, *args, **kwargs):
        item = ItemService.retrieve_item(item_id=kwargs.get("id"))
        return render(request, "index.html", context={"item": item})


class BuyHandler(View):
    def get(self, request, service: BuyServices = buy_services, *args, **kwargs):
        return JsonResponse(
            {
                "session_id": service.get_session(item_id=kwargs.get("id")),
                "key": os.getenv("STRIPE_PUB_KEY"),
            }
        )


class OrderView(View):
    """
    Additional
    Return json with exactly one order
    """

    def get(self, request, *args, **kwargs):
        order = OrderService.retrieve_order(order_id=kwargs.get("id"))
        return JsonResponse(order)


class OrdersByItemView(View):
    """
    Additional
    Return json with several order which include item with passed id
    """

    def get(self, request, *args, **kwargs):
        order = OrderService.retrieve_orders_by_item(item_id=kwargs.get("id"))
        return JsonResponse(order)
