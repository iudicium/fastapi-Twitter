from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, validates
from src.models.base import Base

FILE_TYPES = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".pdf",
    ".epub",
    ".wbep",
    ".txt",
    ".mp4",
    ".mp3",
)


class Media(Base):
    __tablename__ = "media"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    media_path: Mapped[str]
    tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id"), nullable=True)

    @validates("media_path")
    def validate_media_path(self, key, media_path: str) -> str:
        # Check if the file extension is in the FILE_TYPES tuple
        if not media_path.endswith(FILE_TYPES):
            raise ValueError(
                f"Invalid file format. Supported formats: {', '.join(FILE_TYPES)}"
            )

        return media_path

    def __repr__(self):
        return self._repr(
            id=self.id,
            media_path=self.media_path,
            tweet_id=self.tweet_id,
        )
