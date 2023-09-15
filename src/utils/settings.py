from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"
MEDIA_PATH = BASE_DIR / "media"


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_prefix="POSTGRES_",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    HOST: str
    PORT: str
    DB_NAME: str
    USER: str
    PASSWORD: str
    TEST_DB_NAME: str


class ServerSettings(BaseSettings):
    """
    Server-Side configuration for uvicorn
    """

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_prefix="SERVER_",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )
    HOST: str
    PORT: str


@lru_cache()
def get_pg_settings():
    return PostgresSettings()


@lru_cache()
def get_server_settings():
    return ServerSettings()
