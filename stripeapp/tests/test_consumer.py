import pytest
from stripeapp.models import Discount, Tax


@pytest.mark.django_db
@pytest.mark.parametrize(
    "mock_data, model, expected",
    [(Discount, Discount, "coupon"), (Tax, Tax, "tax")],
    indirect=["mock_data"],
)
def test_on_add(mock_manager, mock_data, model, expected):
    obj = model.objects.create(**mock_data)
    assert obj.pk == 1


@pytest.mark.django_db
@pytest.mark.parametrize(
    "mock_data, model, expected",
    [(Discount, Discount, "Coupon"), (Tax, Tax, "Tax")],
    indirect=["mock_data"],
)
def test_on_update(mock_manager, mock_data, capsys, model, expected):
    obj = model.objects.create(**mock_data)
    obj.currency = "usa"
    obj.save()
    captured = capsys.readouterr()
    assert f"{expected} was updated {obj}" == captured.out.split("\n")[0]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "mock_data, model, expected",
    [(Discount, Discount, "Coupon"), (Tax, Tax, "Tax")],
    indirect=["mock_data"],
)
def test_on_delete(mock_manager, mock_data, capsys, model, expected):
    obj = model.objects.create(**mock_data)
    obj.delete()
    obj.save()
    captured = capsys.readouterr()
    assert f"{expected} was deleted" == captured.out.split("\n")[0]
