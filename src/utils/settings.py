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
    LOG_LEVEL: str
    HOST: str
    PORT: str
    DEBUG: bool
    PRODUCTION: bool


class TestSettings(BaseSettings):
    """
    Testing configuration
    """

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_prefix="TEST_",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    DB_NAME: str
    API_KEY: str
    USERNAME: str


class LoggerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_prefix="LOGGER_",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    LEVEL: str
    ROTATION: str
    COMPRESSION: str
    SERIALIZE: bool
    BACKTRACE: bool


@lru_cache()
def get_pg_settings():
    return PostgresSettings()


@lru_cache()
def get_server_settings():
    return ServerSettings()


@lru_cache()
def get_test_settings():
    return TestSettings()


@lru_cache()
def get_logger_settings():
    return LoggerSettings()
