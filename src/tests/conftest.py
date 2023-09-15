from collections.abc import AsyncGenerator
import pytest_asyncio, pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.main import app
from src.utils.settings import get_server_settings
from src.database.database import DATABASE_URL, get_db_session
from src.models.base import Base
from src.models.users import User


server_settings = get_server_settings()
# TODO ADD  below variables to .env
TESTING_API_KEY = "TESTING"
TEST_USERNAME = "testuser"
# TODO UGLY needs fixing


@pytest_asyncio.fixture()
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Start a test database session"""
    # TODO replace this ugly db_name and db_url into a tuple

    db_name = DATABASE_URL.split("/")[-1]
    db_url = DATABASE_URL.replace(f"/{db_name}", "/test")

    engine = create_async_engine(db_url)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session() as session:
        test_user = User(api_key=TESTING_API_KEY, username=TEST_USERNAME)
        session.add(test_user)
        yield session
        await session.delete(test_user)
        await session.commit()


@pytest.fixture()
def test_app(db_session: AsyncSession) -> FastAPI:
    """Create a test app with overridden dependencies."""
    app.dependency_overrides[get_db_session] = lambda: db_session
    return app


@pytest_asyncio.fixture()
async def client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """Create a http client."""
    async with AsyncClient(
        app=test_app,
        base_url=f"http://localhost:{server_settings.PORT}/api/v1",
        headers={"api_key": TESTING_API_KEY},
    ) as client:
        yield client
