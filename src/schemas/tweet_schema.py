from typing import List, Optional
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    HttpUrl,
)

# from pydantic.utils import GetterDict
from src.schemas.base_schema import DefaultSchema
from src.schemas.user_schema import DefaultUser
from src.schemas.media_schema import Media

from src.models.likes import Like as ModelLike
from loguru import logger


# class MediaGetter(GetterDict):
#     def get(self, key: str, default):
#         logger.debug(f"{key}{default}")
#         if hasattr(self._obj, key):
#             return super().get(key, default)
#
#         getter_fun_name = f"get_{key}"
#         if not (getter := getattr(self.model_class, getter_fun_name, None)):
#             raise AttributeError(f"no field getter function found for {key}")
#
#         return getter(self._obj)
#


class Like(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
    user_id: int
    username: Optional[str] = Field(alias="name")

    @field_validator("username", mode="before", check_fields=False)
    @classmethod
    def validate_username(cls, v):
        logger.debug(v)
        return vars(v["user"])


class TweetIn(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]] = list()


class Tweet(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )
    id: int
    tweet_data: str = Field(alias="content")
    media: List[Media] = Field(alias="attachments")
    user: DefaultUser = Field(alias="author")
    likes: List[Like]

    @field_validator("media")
    @classmethod
    def extract_attachments(cls, values: Media):
        media_files = [value for value in values]
        return media_files

    @field_validator("likes")
    @classmethod
    def validate_likes(cls, likes: Like):
        logger.debug(likes)
        return


class TweetOut(DefaultSchema):
    tweets: List[Tweet]
