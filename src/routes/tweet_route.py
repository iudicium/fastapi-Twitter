from typing import Annotated
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.tweet_schema import TweetIn

from src.utils.auth import authenticate_user

from src.models.users import User
from src.database.utils import get_user_by_id, check_follow_user_ability
from src.database.database import get_db_session

router = APIRouter(prefix="/api/v1", tags=["tweets_v1"])



@router.post('/tweets', status_code=status.HTTP_201_CREATED, response_model=TweetIn)
async def  create_tweet(current_user: Annotated[User, "User model obtained from the api key"] = Depends(
        authenticate_user
    ),
    session: AsyncSession = Depends(get_db_session)):

