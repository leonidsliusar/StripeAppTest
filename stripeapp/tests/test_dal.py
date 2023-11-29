import pytest
from stripeapp.dal import add_item, get_item
from stripeapp.tests.conftest import get_item_from_db


@pytest.mark.django_db
@pytest.mark.parametrize('get_stub_item_map, get_stub_item_obj', [(1, 1)],
                         indirect=True)
def test_add_item(get_stub_item_map, get_stub_item_obj):
    add_item(get_stub_item_map)
    assert get_item_from_db(1) == get_stub_item_obj


@pytest.mark.django_db
@pytest.mark.parametrize('add_stub_item, get_stub_item_obj, item_id', [(1, 1, 1)],
                         indirect=['add_stub_item', 'get_stub_item_obj'])
def test_get_item(add_stub_item, get_stub_item_obj, item_id):
    assert get_item(item_id) == get_stub_item_obj
