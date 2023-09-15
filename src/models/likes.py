from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import Base


class Like(Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    tweets_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"), nullable=False)

    def __repr__(self):
        return self._repr(
            id=self.id,
            user_id=self.user_id,
            tweets_id=self.tweets_id,
        )
