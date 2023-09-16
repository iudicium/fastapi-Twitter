from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base import Base
from src.models.tweets import Tweet

# Needed import for creating the media model, sqlalchemy doesn't recognize other models otherwise
from src.models.media import Media
from src.models.likes import Like


class FollowingAssociation(Base):
    __tablename__ = "followers"

    following_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    followers_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    following: Mapped["User"] = relationship(
        back_populates="followers", foreign_keys=[following_id]
    )
    followers: Mapped["User"] = relationship(
        back_populates="following", foreign_keys=[followers_id]
    )

    def __repr__(self):
        return self._repr(
            following_id=self.following_id, followers_id=self.followers_id
        )


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    api_key: Mapped[str]
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    tweets: Mapped[List["Tweet"]] = relationship(
        backref="user", cascade="all, delete-orphan"
    )
    likes: Mapped[List["Like"]] = relationship(
        backref="user", cascade="all, delete-orphan"
    )

    followers: Mapped[List["FollowingAssociation"]] = relationship(
        back_populates="following", foreign_keys=[FollowingAssociation.following_id]
    )
    following: Mapped[List["FollowingAssociation"]] = relationship(
        back_populates="followers", foreign_keys=[FollowingAssociation.followers_id]
    )

    def __repr__(self):
        return self._repr(
            id=self.id,
            api_key=self.api_key,
            username=self.username,
        )
