from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.base_schema import DefaultSchema
from src.schemas.tweet_schema import TweetIn

from src.utils.auth import authenticate_user

from src.models.users import User
from src.models.tweets import Tweet
from src.models.likes import Like

from src.database.utils import (
    associate_media_with_tweet,
    get_tweet_by_id,
    get_like_by_id,
)
from src.database.database import get_db_session

from loguru import logger

router = APIRouter(prefix="/api/v1", tags=["tweets_and_likes_v1"])


@router.post("/tweets", status_code=status.HTTP_201_CREATED, response_model=TweetIn)
async def create_tweet(
    tweet_in: TweetIn,
    current_user: Annotated[User, "User model obtained from the api key"] = Depends(
        authenticate_user
    ),
    session: AsyncSession = Depends(get_db_session),
):
    new_tweet = Tweet(
        user_id=current_user.id,
        tweet_data=tweet_in.tweet_data,
    )
    session.add(new_tweet)
    await session.flush()
    tweet_media_ids = tweet_in.tweet_media_ids

    if tweet_media_ids:
        await associate_media_with_tweet(
            session=session, media_ids=tweet_media_ids, tweet=new_tweet
        )

    await session.commit()
    # TODO Fix later { “result”: true, “tweet_id”: int }

    return new_tweet


@router.delete(
    "/tweets/{tweet_id}", status_code=status.HTTP_200_OK, response_model=DefaultSchema
)
async def delete_tweet(
    tweet_id: int,
    current_user: Annotated[User, "User model obtained from the api key"] = Depends(
        authenticate_user
    ),
    session: AsyncSession = Depends(get_db_session),
):
    tweet_to_delete = await get_tweet_by_id(tweet_id, session)
    if tweet_to_delete.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Regrettably, Your Entry Has Been Met With "
            "an Imposing Barrier, Rendering Further "
            "Passage Unattainable",
        )
    await session.delete(tweet_to_delete)
    await session.commit()
    return tweet_to_delete


@router.post(
    "/tweets/{tweet_id}/likes",
    status_code=status.HTTP_201_CREATED,
    response_model=DefaultSchema,
)
async def like_a_tweet(
    tweet_id: int,
    current_user: Annotated[User, "User model obtained from the api key"] = Depends(
        authenticate_user
    ),
    session: AsyncSession = Depends(get_db_session),
):
    tweet_to_like = await get_tweet_by_id(tweet_id=tweet_id, session=session)
    like = await get_like_by_id(
        session=session, tweet_id=tweet_id, user_id=current_user.id
    )
    if not like:
        like_to_add = Like(user_id=current_user.id, tweet_id=tweet_to_like.id)
        session.add(like_to_add)
        await session.commit()

    return dict()