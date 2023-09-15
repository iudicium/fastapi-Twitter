from typing import Annotated
from fastapi import APIRouter, status, File, UploadFile, Depends


from src.schemas.media_schema import MediaUpload
from src.models.users import User
from src.utils.auth import authenticate_user

router = APIRouter(prefix="/v1", tags=["media_v1"])


@router.post("/medias", status_code=status.HTTP_201_CREATED, response_model=MediaUpload)
async def upload_media(
    api_key: str,
    file: UploadFile,
    user: Annotated[User, "User model obtained from the api key"] = Depends(
        authenticate_user
    ),
):
    pass
