from datetime import datetime

from sqlalchemy import func, String, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column

from . import Base
from utils.pass_hash import hash_password, verify_password

class UserTable(Base):

    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(String(150))
    is_verified: Mapped[bool] = mapped_column(insert_default=False)
    join_data: Mapped[datetime] = mapped_column(insert_default=func.now())

    @classmethod
    async def create(cls, db: AsyncSession, **new_user: dict):
        # ? gets
        transaction = cls(**new_user)
        transaction.password = hash_password(transaction.password)
        db.add(transaction)
        await db.commit()
        await db.refresh(transaction)
        return transaction

    @classmethod
    async def get(cls, db: AsyncSession, id: str):
        try:
            transaction = await db.get(cls, id)
        except NoResultFound as e:
            return None

        return transaction

    @classmethod
    async def authenticate_user(cls, db: AsyncSession, email, password):
        try:
            user = await cls.get_by_email(db, email)
            if not user:
                return None
            # ? Hashed password verification
            pass_result = verify_password(password, user.password)

            if not pass_result:
                return None

            return True
        except NoResultFound as e:
            return None

    @classmethod
    async def get_by_email(cls, db: AsyncSession, email: str):
        try:
            stmt = select(cls).where(cls.email == email)
            results = await db.execute(stmt)
            # ? Is better to store results first, and then access
            transaction = results.scalars().one()
        except NoResultFound as e:
            return None

        return transaction

    @classmethod
    async def get_all(cls, db: AsyncSession):
        try:
            result = await db.execute(select(cls))
            transaction = result.scalars().all()
        except NoResultFound as e:
            return None

        return transaction

    @classmethod
    async def get_verified_user(cls, db: AsyncSession, email: str) -> bool:
        db_user = cls.get_by_email(db, email)
        if not db_user:
            return False
        if db_user.is_verified:
            return True
        return False

    @classmethod
    async def update(cls, db: AsyncSession,  id: str, **update_user: dict):
        db_user = await cls.get(db, id)
        print('DB USER',db_user)
        print('Update User',update_user)
        if not db_user:
            return None

        # ? Method 1 - Using SQLAlchemy ORM statements
        # stmt = (
        #     update(UserTable)
        #     .where(UserTable.id == id)
        #     .values(email=update_user['email'])
        # )
        # await db.execute(stmt)

        # ? Method 2 - Updating field by field
        # db_user.email = update_user['email']
        # if update_user['password'] != '':
        #     db_user.password = update_user['password']

        # ? Method 3 - Dynamic assignation with dictionary
        # print(update_user)
        for key, value in update_user.items():
            if value == '':
                continue
            setattr(db_user, key, value)

        await db.commit()
        await db.refresh(db_user)
        return db_user
