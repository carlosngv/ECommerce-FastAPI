from sqlalchemy.ext.asyncio import AsyncSession
from models import UserTable
from schemas import User, UserCreate

async def add_user(user: UserCreate, db: AsyncSession):
    user = await UserTable.create(db, **user.model_dump())
    pass
