from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_db_session
from src.database.utils import get_user_by_api_key

API_KEY_HEADER = APIKeyHeader(name="api_key")


async def authenticate_user(
    api_key: str = Security(API_KEY_HEADER),
    session: AsyncSession = Depends(get_db_session),
):
    """Check if user exists otherwise raise errors
    @TODO maybe i should rename the function to something better
    """
    user = await get_user_by_api_key(api_key, session)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key authentication failed",
        )

    return user
