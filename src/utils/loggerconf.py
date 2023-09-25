from sys import stdout

from fastapi import Request
from loguru import logger

from src.utils.settings import BASE_DIR, get_logger_settings

settings = get_logger_settings()


def get_logger() -> None:
    log_path = BASE_DIR / "logs/logs.log"
    logger.remove()
    logger.add(
        log_path,
        level=settings.LEVEL,
        rotation=settings.ROTATION,
        compression=settings.COMPRESSION,
        backtrace=settings.BACKTRACE,
        serialize=settings.SERIALIZE,
    )
    logger.add(stdout, level=settings.LEVEL, colorize=True)


async def logging_dependency(request: Request) -> None:
    """Simple class for logging each request"""

    logger.debug(f"{request.method} {request.url}")
    logger.debug("Params:")
    for name, value in request.path_params.items():
        logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")
