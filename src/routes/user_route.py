from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger


from src.schemas.base_schema import BaseShema
from src.models.users import User, FollowingAssociation

from src.utils.auth import authenticate_user

from src.database.utils import get_user_by_id, check_follow_user_ability
from src.database.database import get_db_session

router = APIRouter(prefix="/api/v1", tags=["users_v1"])


@router.post(
    "/users/{user_id}/follow",
    status_code=status.HTTP_201_CREATED,
    response_model=BaseShema,
)
async def follow_user(
    user_id: int,
    current_user: Annotated[User, "User model obtained from the api key"] = Depends(
        authenticate_user
    ),
    session: AsyncSession = Depends(get_db_session),
):
    logger.info(
        f"User being followed {user_id} || User who's following:  {current_user.id}"
    )
    try:
        user_to_follow = await get_user_by_id(user_id, session)
        following_ability = await check_follow_user_ability(
            current_user, user_to_follow, session
        )

        if following_ability:
            follower_association = FollowingAssociation(
                following=user_to_follow, followers=current_user
            )
            user_to_follow.followers.append(follower_association)

            await session.commit()

        return {"result": True}

    except ValueError as exc:
        logger.exception(exc)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Oops. Something went wrong"
        )
