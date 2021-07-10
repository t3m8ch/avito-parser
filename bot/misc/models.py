from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class SubscriptionModel(BaseModel):
    id: Optional[int]
    chat_id: int
    url: str


class AdModel(BaseModel):
    title: str
    price: Optional[Decimal]
    url: str
    subscription: Optional[SubscriptionModel]
