from src.schemas.base_schema import BaseShema, ConfigDict


class MediaUpload(BaseShema):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    media_id: int
