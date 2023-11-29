import json

from stripeapp.dal import add_item, get_item
from stripeapp.datamodels import ItemModel
from stripeapp.paymentAPI.manager import PaymentManager, StripeManager


class ItemService:

    @staticmethod
    def new_item(item: json) -> None:
        add_item(item)

    @staticmethod
    def retrieve_item(item_id: int) -> dict:
        item_from_db = get_item(item_id)
        item = ItemModel(**item_from_db.__dict__).model_dump()
        return item


class BuyServices:

    def __init__(self, payment_system: PaymentManager = StripeManager()):
        self.payment_manager = payment_system

    def get_session(self, item_id: int) -> dict:
        item_obj_map = ItemService.retrieve_item(item_id)
        return {"session": self.payment_manager.get_session(item=item_obj_map)}


buy_services = BuyServices()
