from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from src.models.base import Base


class FollowingAssociation(Base):
    __tablename__ = "followers"

    following_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    followers_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    api_key: Mapped[str]
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)

    followers: Mapped[List[FollowingAssociation]] = relationship(
        "FollowingAssociation", back_populates="user"
    )
