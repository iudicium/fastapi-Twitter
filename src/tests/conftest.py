from collections.abc import AsyncGenerator
import asyncio
import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.main import app
from src.database.database import DATABASE_URL
from src.models.base import Base


@pytest.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Start a test database session."""
    db_name = DATABASE_URL.split("/")[-1]
    print(db_name)
    db_url = DATABASE_URL.replace(f"/{db_name}", "/test")

    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    session = async_sessionmaker(engine)()
    yield session
    await session.close()


async def test_main(db_session):
    pass
