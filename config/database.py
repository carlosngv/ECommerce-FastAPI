import os

from contextlib import asynccontextmanager
from typing import Any, AsyncIterator
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    AsyncEngine,
    async_sessionmaker,
    create_async_engine
)

from models import Base

SQLITE_DB_FILE = '../database.sqlite3'
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DB_URL = f'sqlite+aiosqlite:///{os.path.join(BASE_DIR, SQLITE_DB_FILE)}'

class DataBaseSessionManager:

    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}) -> None:
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        if self._engine is None:
            raise Exception('DataBaseSessionManager is not initialized')
        await self._engine.disponse()
        self._engine = None
        self._sessionmaker = None

    @asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception('DataBaseSessionManager is not initialized')

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception('DataBaseSessionManager is not initialized')

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


    async def create_all(self, connection: AsyncConnection) -> None:
        await connection.run_sync(Base.metadata.create_all)

    async def drop_all(self, connection: AsyncConnection) -> None:
        await connection.run_sync(Base.metadata.drop_all)

sessionmanager = DataBaseSessionManager(DB_URL, {'echo': True})


async def get_db():
    async with sessionmanager.session() as session:
        yield session

async def create_tables():
    async with sessionmanager.connect() as connection:
        await sessionmanager.create_all(connection)
