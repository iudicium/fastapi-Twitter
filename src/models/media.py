from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import ForeignKey
from src.models.base import Base


class Media(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    media_path: Mapped[str]
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"), nullable=True)

    @validates("media_path")
    def validate_media_path(self, key, media_path: str) -> str:
        # TODO add more media  later
        if not media_path.endswith((".jpg", ".jpeg", ".png", ".gif")):
            raise ValueError(
                "Invalid file format. Supported formats: .jpg, .jpeg, .png, .gif"
            )

        return media_path
