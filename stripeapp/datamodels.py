from dataclasses import dataclass
from typing import Optional

from pydantic import BaseModel


class ItemModel(BaseModel):
    id: Optional[int]
    name: str
    description: str
    price: int
