from datetime import datetime

from pydantic import (
    BaseModel,
    Field
)
from typing import Annotated, Optional


class Product(BaseModel):
    id: Optional[int] = None
    name: Annotated[str, Field(min_length=4, max_length=15)]
    category: Annotated[str, Field(min_length=4, max_length=15)]
    original_price: float
    new_price: float
    percentage_discount: int
    offer_expiration_date: datetime
    product_image: str
    business: Optional[int] = None
