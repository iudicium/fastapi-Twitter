from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.utils.settings import PostgresSettings, get_pg_settings
from sqlalchemy.exc import SQLAlchemyError

from loguru import logger

settings: PostgresSettings = get_pg_settings()

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.USER}:{settings.PASSWORD}@"
    f"{settings.HOST}:{settings.PORT}/{settings.DB_NAME}"
)


engine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as error:
            await session.rollback()
            logger.exception(error)
