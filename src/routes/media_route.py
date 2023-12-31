from typing import Annotated, Union

from fastapi import APIRouter, Depends, HTTPException, UploadFile, status
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database import get_db_session
from src.models.media import Media
from src.models.users import User
from src.schemas.media_schema import MediaUpload
from src.utils.auth import authenticate_user
from src.utils.file_utils import save_uploaded_file

router = APIRouter(prefix="/api", tags=["media_v1"])


@router.post("/medias", status_code=status.HTTP_201_CREATED, response_model=MediaUpload)
async def upload_media(
    file: UploadFile,
    user: Annotated[User, "User model obtained from the api key"] = Depends(
        authenticate_user
    ),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        file = await save_uploaded_file(file)
        new_media = Media(media_path=file)
        session.add(new_media)
        await session.commit()

        return new_media
    except ValueError as exc:
        logger.exception(exc)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
