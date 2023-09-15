from typing import List

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyBaseAccessTokenTable
from src.models.base import Base
from src.models.tweets import Tweet

# Needed import for creating the media model, sqlalchemy doesn't recognize other models otherwise
from src.models.media import Media
from src.models.likes import Like


class FollowingAssociation(Base):
    __tablename__ = "followers"

    following_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    followers_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class User(SQLAlchemyUserDatabase, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    api_key: Mapped[str]
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    tweets: Mapped[List[Tweet]] = relationship(
        backref="user", cascade="all, delete-orphan"
    )
    likes: Mapped[List[Like]] = relationship(
        backref="user", cascade="all, delete-orphan"
    )
    followers: Mapped[List[FollowingAssociation]] = relationship(
        "FollowingAssociation", back_populates="user"
    )

    def __repr__(self):
        return self._repr(
            id=self.id,
            api_key=self.api_key,
            username=self.username,
        )


class AccessToken(SQLAlchemyBaseAccessTokenTable[int], Base):
    __tablename__ = "auth_token"

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False
        )
