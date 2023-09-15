from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.database.database import engine, get_db_session
from src.models.users import Base, User


async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_user_by_api_key(
    api_key: str, session: AsyncSession = Depends(get_db_session)
):
    query = (
        select(User)
        .where(User.api_key == api_key)
        .options(
            selectinload(User.followers),
            selectinload(User.following),
        )
    )
    user = await session.execute(query)
    return user.scalar_one_or_none()
