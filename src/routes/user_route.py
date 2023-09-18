from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_db_session
from src.database.utils import check_follow_user_ability, get_user_by_id
from src.models.users import User
from src.schemas.base_schema import DefaultSchema
from src.schemas.user_schema import UserOutSchema
from src.utils.auth import authenticate_user

router = APIRouter(prefix="/api/v1", tags=["users_v1"])


# Endpoint has to be here otherwise it will be 422 unprocessable
# entity, as the router after that registers "me" as an integer
@router.get("/users/me", status_code=status.HTTP_200_OK, response_model=UserOutSchema)
async def get_info_about_me(
    current_user: Annotated[User, "User model obtained from the api key"] = Depends(
        authenticate_user
    ),
):
    return {"user": current_user}


@router.get(
    "/users/{user_id}", status_code=status.HTTP_200_OK, response_model=UserOutSchema
)
async def get_info_of_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_db_session),
    current_user: Annotated[User, "User model obtained from the api key"] = Depends(
        authenticate_user
    ),
):
    user = await get_user_by_id(user_id, session)

    return {"user": user}


@router.post(
    "/users/{user_id}/follow",
    status_code=status.HTTP_201_CREATED,
    response_model=DefaultSchema,
)
async def follow_user(
    user_id: int,
    current_user: Annotated[User, "User model obtained from the api key"] = Depends(
        authenticate_user
    ),
    session: AsyncSession = Depends(get_db_session),
):
    user_to_follow = await get_user_by_id(user_id, session)
    following_ability = await check_follow_user_ability(current_user, user_to_follow)

    if following_ability:
        user_to_follow.followers.append(current_user)
        await session.commit()
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You already follow that user!",
        )
    return {"result": True}


@router.delete(
    "/users/{user_id}/follow",
    status_code=status.HTTP_200_OK,
    response_model=DefaultSchema,
)
async def unsubscribe_from_user(
    user_id: int,
    current_user: Annotated[User, "User model obtained from the api key"] = Depends(
        authenticate_user
    ),
    session: AsyncSession = Depends(get_db_session),
):
    follower_deleted = await get_user_by_id(user_id, session)

    if follower_deleted not in current_user.following:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are not following this user.",
        )

    current_user.following.remove(follower_deleted)
    await session.commit()
    return {"result": True}
