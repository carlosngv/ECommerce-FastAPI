from sqlalchemy.orm import DeclarativeBase, registry

reg = registry()

class Base(DeclarativeBase):
    registry = reg

from .user import UserTable
from .product import ProductTable
from .business import BusinessTable
