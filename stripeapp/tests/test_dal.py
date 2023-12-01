import pytest
from stripeapp.dal import add_item, get_item, get_order, get_orders_by_item
from stripeapp.datamodels import OrderDTO
from stripeapp.tests.conftest import get_item_from_db


@pytest.mark.django_db
@pytest.mark.parametrize(
    "get_stub_item_map, get_stub_item_obj", [(1, 1)], indirect=True
)
def test_add_item(get_stub_item_map, get_stub_item_obj):
    add_item(get_stub_item_map)
    assert get_item_from_db(1) == get_stub_item_obj


@pytest.mark.django_db
@pytest.mark.parametrize(
    "add_stub_item, get_stub_item_obj, item_id",
    [(1, 1, 1)],
    indirect=["add_stub_item", "get_stub_item_obj"],
)
def test_get_item(add_stub_item, get_stub_item_obj, item_id):
    assert get_item(item_id) == get_stub_item_obj


@pytest.mark.django_db
def test_get_order(stub_order, stub_order_map):
    expected_map = OrderDTO(**stub_order_map)
    obj_map = OrderDTO.serialize_django_model(get_order(stub_order.pk)).model_dump(exclude_none=True)
    assert obj_map == expected_map.model_dump(exclude_none=True)


@pytest.mark.django_db
def test_get_order_by_item(stub_order, stub_order_map):
    assert stub_order.pk == 1
    expected_map = OrderDTO(**stub_order_map)
    obj_set = OrderDTO.serialize_django_model(get_orders_by_item(stub_order.pk))
    obj_map_set = [obj.model_dump(exclude_none=True) for obj in obj_set]
    assert obj_map_set == [expected_map.model_dump(exclude_none=True)]