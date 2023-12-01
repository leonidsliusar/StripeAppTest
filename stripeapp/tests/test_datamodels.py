from decimal import Decimal

import pytest

from stripeapp.datamodels import DiscountDTO, TaxDTO, DiscountDTOUpdate
from stripeapp.models import Discount, Tax


@pytest.mark.parametrize("mock_data", (Discount,), indirect=True)
def test_DiscountDTO(mock_data):
    obj = DiscountDTO.model_validate(mock_data)
    obj_dto = obj.model_dump(exclude_none=True)
    obj_dto_id = obj_dto.pop("id")
    mock_data_id = mock_data.pop("id")
    mock_data.pop("redeem_by")
    mock_data.update({"duration": "once"})
    assert obj_dto == mock_data
    assert obj_dto_id == str(mock_data_id)


@pytest.mark.parametrize("mock_data", (Tax,), indirect=True)
def test_TaxDTO(mock_data):
    obj_dto = TaxDTO.model_validate(mock_data).model_dump(exclude_none=True)
    mock_data['active'] = True
    mock_data['id'] = str(mock_data['id'])
    assert obj_dto == mock_data


@pytest.mark.parametrize("mock_data", (Discount,), indirect=True)
def test_DiscountDTOUpdate(mock_data):
    obj = DiscountDTOUpdate.model_validate(mock_data)
    obj_dto = obj.model_dump(exclude_none=True)
    mock_data_for_update = {
        "id": str(mock_data.pop("id")),
        "metadata": mock_data.pop("metadata"),
    }
    assert obj_dto == mock_data_for_update
