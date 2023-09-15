from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class Tweet(Base):
    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    create_date: Mapped[datetime] = mapped_column(server_default=func.now())
    tweet_data: Mapped[str] = mapped_column(String(2500))
    media: Mapped[List["Media"]] = relationship(
        backref="tweets", cascade="all, delete-orphan"
    )
    likes: Mapped[List["Like"]] = relationship(
        backref="tweets", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return self._repr(
            id=self.id,
            user_id=self.user_id,
            create_date=self.create_date,
            tweet_data=self.tweet_data,
        )
