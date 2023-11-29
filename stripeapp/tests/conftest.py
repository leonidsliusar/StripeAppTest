import os
import time
import pytest
from stripeapp.models import Item


@pytest.fixture(scope="module")
def django_db_setup():
    os.system('docker compose -f stripeapp/tests/docker-compose.yml up -d')
    time.sleep(2)
    os.system('python manage.py migrate')
    yield
    os.system('docker compose -f stripeapp/tests/docker-compose.yml down -v')


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
    Item.objects.create(**stub_item_map(request.param))


def stub_item_map(item_inx: int) -> dict:
    return {
        'id': item_inx,
        'name': f'testItem_{item_inx}',
        'description': 'foo',
        'price': 1
    }
