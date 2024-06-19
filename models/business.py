from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import BusinessCreate

from . import Base

class BusinessTable(Base):
    __tablename__ = 'business'
    id: Mapped[int] = mapped_column(primary_key=True)
    business_name: Mapped[str]
    city: Mapped[str]
    region: Mapped[str]
    business_description: Mapped[str]
    logo: Mapped[str]
    owner: Mapped[str]

    @classmethod
    async def create(db: AsyncSession,):
        pass
