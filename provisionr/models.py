from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy import ForeignKey
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

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


class Team(Base):
    __tablename__ = "team"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    members: Mapped[list["Person"]] = relationship(back_populates="team")


class Person(Base):
    __tablename__ = "person"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    maintainer: Mapped[bool]

    team_id: Mapped[int] = mapped_column(ForeignKey("team.id"))
    team: Mapped["Team"] = relationship(back_populates="members")

