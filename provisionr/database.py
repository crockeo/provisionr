from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from provisionr.utils import async_cache


@async_cache
async def create_engine() -> AsyncEngine:
    async_engine = create_async_engine("sqlite+aiosqlite:///database.sqlite3")
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return async_engine


@asynccontextmanager
async def create_session(engine: AsyncEngine | None = None) -> AsyncGenerator[AsyncSession, None]:
    if engine is None:
        engine = await create_engine()
    async with AsyncSession(engine, expire_on_commit=False) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


class Base(DeclarativeBase):
    pass

