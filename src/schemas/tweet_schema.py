from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from src.schemas.base_schema import DefaultSchema


class TweetIn(BaseModel):
    tweet_data: str
    tweet_media_ids: Optional[List[int]]


class TweetOut(DefaultSchema):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
    id: int
