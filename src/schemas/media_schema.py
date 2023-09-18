from pydantic import BaseModel
from src.schemas.base_schema import DefaultSchema, ConfigDict


class MediaUpload(DefaultSchema):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    media_id: int


class Media(BaseModel):
    media_path: str
