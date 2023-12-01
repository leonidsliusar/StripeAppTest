import os
import time
from datetime import datetime, timezone
from decimal import Decimal

import pytest
from stripeapp.models import Item, Discount, Order, Tax


@pytest.fixture()
def mock_manager(mocker):
    mock_inst = mocker.Mock()
    mock_inst.new_coupon.return_value = {"id": 1}
    mock_inst.update_coupon.side_effect = lambda instance, *args, **kwargs: print(
        f"Coupon was updated {instance}"
    )
    mock_inst.delete_coupon.side_effect = lambda instance_id, *args, **kwargs: print(
        f"Coupon was deleted"
    )
    mock_inst.new_tax.return_value = {"id": 1}
    mock_inst.update_tax.side_effect = lambda instance, *args, **kwargs: print(
        f"Tax was updated {instance}"
    )
    mock_inst.delete_tax.side_effect = lambda instance_id, *args, **kwargs: print(
        f"Tax was deleted"
    )
    mocker.patch(
        "stripeapp.signals.consumer.StripeManagerExtend", return_value=mock_inst
    )
    return mock_inst


@pytest.fixture()
def mock_data(request) -> dict:
    model = request.param
    discount_map = stub_discount_map()
    tax_map = stub_tax_map()
    return discount_map if model is Discount else tax_map


@pytest.fixture(scope="session")
def django_db_setup():
    os.system("docker compose -f stripeapp/tests/docker-compose.yml up -d")
    time.sleep(2)
    os.system("python manage.py migrate")
    yield
    os.system("docker compose -f stripeapp/tests/docker-compose.yml down -v")


def get_item_from_db(obj_id: int) -> Item:
    obj = Item.objects.get(id=obj_id)
    return obj


@pytest.fixture()
def get_stub_item_map(request) -> dict:
    return stub_item_map(request.param)


@pytest.fixture()
def get_stub_item_obj(request) -> Item:
    return Item(**stub_item_map(request.param))


@pytest.fixture()
def add_stub_item(request):
    obj = Item.objects.create(**stub_item_map(request.param))
    return obj


def stub_item_map(item_inx: int) -> dict:
    return {
        "id": item_inx,
        "name": f"testItem_{item_inx}",
        "description": "foo",
        "price": 1,
    }


def stub_discount_map() -> dict:
    return {
        "id": "1",
        "currency": "eur",
        "percent_off": 50.5,
        "max_redemptions": 2,
        "redeem_by": datetime(year=2050, month=1, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc),
        "metadata": {"1": "1"},
    }


def stub_tax_map() -> dict:
    return {
        "id": 1,
        "display_name": "tax",
        "inclusive": True,
        "percentage": 15.5,
        "description": "desc",
    }


@pytest.fixture()
def stub_order_map() -> dict:
    return {
        "id": 1,
        "items": [stub_item_map(1)],
        "discount": stub_discount_map(),
        "tax": stub_tax_map()
    }


@pytest.fixture(scope='function')
def stub_order(mocker) -> Order:
    mock_inst = mocker.Mock()
    mock_inst.new_coupon.return_value = {"id": 1}
    mock_inst.update_coupon.side_effect = lambda instance, *args, **kwargs: print(
        f"Coupon was updated {instance}"
    )
    mock_inst.delete_coupon.side_effect = lambda instance_id, *args, **kwargs: print(
        f"Coupon was deleted"
    )
    mock_inst.new_tax.return_value = {"id": 1}
    mock_inst.update_tax.side_effect = lambda instance, *args, **kwargs: print(
        f"Tax was updated {instance}"
    )
    mock_inst.delete_tax.side_effect = lambda instance_id, *args, **kwargs: print(
        f"Tax was deleted"
    )
    mocker.patch(
        "stripeapp.signals.consumer.StripeManagerExtend", return_value=mock_inst
    )
    item = Item.objects.create(**stub_item_map(1))
    item.save()
    discount = Discount.objects.create(**stub_discount_map())
    tax = Tax.objects.create(**stub_tax_map())
    order = Order.objects.create(id=1)
    order.items.add(item)
    order.discount = discount
    order.tax = tax
    order.save()
    return order
