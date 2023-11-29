import os

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from stripeapp.services import ItemService, buy_services, BuyServices


class ItemView(View):

    def get(self, request, *args, **kwargs):
        item = ItemService.retrieve_item(item_id=kwargs.get('id'))
        stripe_pub_key = os.getenv('STRIPE_PUB_KEY')
        return render(request, 'index.html', context={'item': item, 'key': stripe_pub_key})


class BuyHandler(View):

    def get(self, request, service: BuyServices = buy_services, *args, **kwargs):
        return JsonResponse({"id": service.get_session(item_id=kwargs.get('id'))})
