from pydantic import (
    BaseModel,
    Field
)
from typing import Annotated, Optional


class Business(BaseModel):
    id: Optional[int] = None
    business_name: Annotated[str, Field(min_length=8, max_length=25)]
    city: str
    region: str
    business_description: Annotated[str, Field(min_length=10, max_length=50)]
    logo: str
    owner: str
