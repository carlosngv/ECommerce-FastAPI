from datetime import datetime

from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column

from . import Base

class UserTable(Base):

    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = String()
    is_verified: Mapped[bool]
    join_data: Mapped[datetime] = mapped_column(insert_default=func.now())
