import datetime
from decimal import Decimal
from typing import Optional, Any, TypeVar, Union
from pydantic import BaseModel, field_validator, Field, model_validator
from stripeapp.models import Discount, Item, Tax, Order


class ItemDTO(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    price: int


class DiscountDTO(BaseModel):
    id: str
    currency: str
    duration: Optional[str] = "once"
    percent_off: float
    duration_in_months: Optional[int] = None
    name: Optional[str] = None
    max_redemptions: Optional[int] = None
    redeem_by: Optional[datetime.datetime]
    metadata: Optional[dict] = None

    @field_validator("id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        return str(value)

    @field_validator("redeem_by", mode="after")
    def check_data(cls, value) -> datetime.datetime:
        if value and value < datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=5 * 365):
            return value

    @field_validator("metadata", mode="after")
    def transform_metadata_items(cls, data) -> dict:
        if data:
            return {str(key): str(value) for key, value in data.items()}


class DiscountDTOUpdate(BaseModel):
    id: str
    name: Optional[str] = None
    metadata: Optional[dict] = None

    @field_validator("id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        return str(value)


class TaxBase(BaseModel):
    id: Optional[str] = Field(alias='pk', default=None)
    active: bool = True
    country: Optional[str] = None
    description: Optional[str] = None
    display_name: Optional[str] = None
    jurisdiction: Optional[str] = None
    state: Optional[str] = None
    metadata: Optional[dict] = None

    @field_validator("id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value:
            return str(value)

    @field_validator("metadata", mode="after")
    def transform_metadata_items(cls, data) -> dict:
        if data:
            return {str(key): str(value) for key, value in data.items()}


class TaxDTO(TaxBase):

    id: Optional[str] = None
    display_name: str
    percentage: Decimal = Field(ge=0, le=100, decimal_places=3)
    inclusive: bool = False

    @field_validator("percentage", mode="before")
    def serialize_decimal(cls, data: Decimal) -> Decimal:
        if data:
            data = Decimal(data)
            data = data.quantize(Decimal('.001'))
            return data


class TaxDTOUpdate(TaxBase):
    ...


TOrderDTO = TypeVar('TOrderDTO', bound='OrderDTO')


class OrderDTO(BaseModel):
    id: int
    items: list[Optional[ItemDTO]]
    discount: Optional[DiscountDTO]
    tax: Optional[TaxDTO]

    @classmethod
    def serialize_django_model(cls, data: Union[Order, list[Order]]) -> Union[TOrderDTO, list[TOrderDTO]]:
        if isinstance(data, list):
            serialized_data = [cls.serialize_django_model(order) for order in data]
            return serialized_data
        else:
            order_map = {
                "id": data.pk,
                "items": [item.__dict__ for item in data.items.all()],
                "discount": data.discount.__dict__ if data.discount else None,
                "tax": data.tax.__dict__ if data.tax else None
            }
            return OrderDTO(**order_map)
