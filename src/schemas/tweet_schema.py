from typing import List, Optional


from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from src.models.likes import Like as LikeModel
from src.schemas.base_schema import DefaultSchema
from src.schemas.media_schema import Media
from src.schemas.user_schema import DefaultUser


class Like(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
    user_id: int
    username: str = Field(alias="name")

    @model_validator(mode="before")
    @classmethod
    def validate_model(self, data: LikeModel) -> "Like":
        """Field username does not actually exist on our model, because
        it is  a relationship to the user, we have to construct the model"""
        return Like.model_construct(user_id=data.user_id, username=data.user.username)


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

    @field_validator("media", mode="after")
    @classmethod
    def extract_attachments(cls, values: Media):
        media_files = [value for value in values]
        return media_files


class TweetOut(DefaultSchema):
    tweets: List[Tweet]
