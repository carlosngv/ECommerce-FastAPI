from datetime import datetime

from . import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

class ProductTable(Base):
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    category: Mapped[str]
    original_price: Mapped[float]
    new_price: Mapped[float]
    percentage_discount: Mapped[int]
    offer_expiration_date: Mapped[datetime]
    product_image: Mapped[str]
    business: Mapped[int] = mapped_column(ForeignKey('business.id'))
