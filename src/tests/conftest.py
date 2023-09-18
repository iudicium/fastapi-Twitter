from collections.abc import AsyncGenerator
from typing import Dict

import pytest
import pytest_asyncio
from faker import Faker
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.database.database import DATABASE_URL, get_db_session
from src.main import app
from src.models.base import Base
from src.models.tweets import Tweet
from src.models.users import User
from src.utils.settings import get_server_settings, get_test_settings

server_settings = get_server_settings()
testing_settings = get_test_settings()
# Need this for easy clean up of media folder, and I don't have to import the whole settings
TEST_USERNAME = testing_settings.USERNAME


valid_tweet_timeline_structure: Dict = {
    "result": True,
    "tweets": [
        {
            "id": 3,
            "content": "Sense peace economy travel.",
            "attachments": [{"media_path": "image.jpg"}],
            "author": {"id": 4, "name": "fake_user3"},
            "likes": [{"user_id": 1, "name": "testuser"}],
        }
    ],
}

unauthorized_structure_response: Dict = {
    "result": False,
    "error_type": "Unauthorized",
    "error_message": "API key authentication failed",
}


@pytest_asyncio.fixture()
async def db_session() -> AsyncSession:
    db_name = DATABASE_URL.split("/")[-1]
    db_url = DATABASE_URL.replace(f"/{db_name}", f"/{testing_settings.DB_NAME}")
    engine = create_async_engine(db_url)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        # Main test runner user

        test_user = User(api_key=testing_settings.API_KEY, username=TEST_USERNAME)
        session.add(test_user)

        fake_users = [
            User(api_key=f"fake_api_key{i}", username=f"fake_user{i}")
            for i in range(1, 6)
        ]

        session.add_all(fake_users)

        yield session
        await session.close()


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
        headers={"api_key": testing_settings.API_KEY},
    ) as client:
        yield client


@pytest_asyncio.fixture()
async def invalid_client(test_app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(
        app=test_app,
        base_url=f"http://localhost:{server_settings.PORT}/api/v1",
        headers={"api_key": "unauthorized"},
    ) as client:
        yield client


@pytest_asyncio.fixture()
async def create_random_tweets(
    client: AsyncClient, faker: Faker, db_session: AsyncSession
):
    for user_id in range(2, 6):
        new_tweet = Tweet(
            user_id=user_id,
            tweet_data=faker.sentence(),
        )
        db_session.add(new_tweet)
