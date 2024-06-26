from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession

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
    async def create(cls, db: AsyncSession, **new_business: dict):
        transaction = cls(**new_business)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return True

    @classmethod
    async def get(cls, id: int, db: AsyncSession):
        db_business = await db.get(cls, id)
        if not db_business:
            return None
        return db_business

    @classmethod
    async def update(cls, db: AsyncSession, id: int, **new_business: dict) -> bool:
        db_business = await cls.get(id, db)
        if not db_business:
            return False
        for key, value in new_business.items():
            setattr(db_business, key, value)

        await db.commit()
        await db.refresh(db_business)
        return True

    @classmethod
    async def get_all(cls, db: AsyncSession):
        try:
            transaction = await db.execute(select(cls))
            result =  transaction.scalars().all()
            return result
        except:
            return None
