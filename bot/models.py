from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class AdModel(BaseModel):
    title: str
    price: Optional[Decimal]
    url: str


class SubscriptionModel(BaseModel):
    chat_id: int
    url: str
