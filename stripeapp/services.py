from typing import Union

from stripeapp.dal import add_item, get_item, get_order, get_orders_by_item
from stripeapp.datamodels import ItemDTO, OrderDTO, TaxDTO
from stripeapp.paymentAPI.manager import PaymentManager, StripeManager


class ItemService:
    @staticmethod
    def new_item(item: dict) -> None:
        add_item(item)

    @staticmethod
    def retrieve_item(item_id: int) -> dict:
        item_from_db = get_item(item_id)
        item = ItemDTO.model_validate(item_from_db.__dict__).model_dump(
            exclude_none=True
        )
        return item


class OrderService:
    @staticmethod
    def retrieve_order(order_id: Union[str, int]) -> dict:
        order_from_db = get_order(order_id)
        order = OrderDTO.serialize_django_model(order_from_db).model_dump(
            exclude_none=True
        )
        return order

    @staticmethod
    def retrieve_orders_by_item(item_id: Union[str, int]) -> list[dict]:
        orders_from_db = get_orders_by_item(item_id)
        obj_set = OrderDTO.serialize_django_model(orders_from_db)
        obj_map_set = [obj.model_dump(exclude_none=True) for obj in obj_set]
        return obj_map_set


class BuyServices:
    def __init__(self, payment_system: PaymentManager = StripeManager()):
        self.payment_manager = payment_system

    def get_session(self, item_id: int) -> str:
        item_obj_map = ItemService.retrieve_item(item_id)
        return self.payment_manager.get_session(item=item_obj_map)


buy_services = BuyServices()
