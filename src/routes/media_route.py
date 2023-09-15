from fastapi import APIRouter, status, File, UploadFile
from src.schemas.media_schema import MediaUpload

router = APIRouter(prefix="/v1", tags=["v1"])


@router.post("/medias", status_code=status.HTTP_201_CREATED, response_model=MediaUpload)
async def upload_media(api_key: str, file: UploadFile):
    pass
