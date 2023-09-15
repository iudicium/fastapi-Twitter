from src.schemas.base_schema import BaseShema


class MediaUpload(BaseShema):
    media_id: int

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
