from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from src.models.base import Base


class Tweet(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    tweet_data: Mapped[str] = mapped_column(String(2500))
