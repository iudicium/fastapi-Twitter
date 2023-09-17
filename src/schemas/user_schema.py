from typing import List, Optional
from pydantic import BaseModel, ConfigDict
from src.schemas.base_schema import DefaultSchema


class DefaultUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str


class User(DefaultUser):
    model_config = ConfigDict(from_attributes=True)
    followers: List[DefaultUser]
    following: List[DefaultUser]


class UserOutSchema(DefaultSchema):
    user: User
