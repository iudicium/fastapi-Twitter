from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.database.database import engine, get_db_session
from src.models.users import Base, User, FollowingAssociation
from loguru import logger


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


async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_db_session)):
    query = (
        select(User)
        .where(User.id == user_id)
        .options(
            selectinload(User.followers),
            selectinload(User.following),
        )
    )
    user = await session.execute(query)

    return user.scalar_one_or_none()


async def check_follow_user_ability(
    current_user: User,
    user_being_followed: User,
    session: AsyncSession = Depends(get_db_session()),
) -> bool:
    """Check if the following requests matches all the criteria"""
    if not user_being_followed:
        logger.info("User does not exist")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )

    elif user_being_followed.id == current_user.id:
        logger.info(f"User {current_user} tried to follow himself")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unable to follow yourself"
        )

    else:
        is_following = await session.execute(
            select(FollowingAssociation).filter(
                FollowingAssociation.following_id == user_being_followed.id,
                FollowingAssociation.followers_id == current_user.id,
            )
        )
        if is_following.scalar():
            logger.info(f"User {current_user} already follows {user_being_followed}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You already follow that user!",
            )

    return True
