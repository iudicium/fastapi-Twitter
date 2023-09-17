from sys import stdout
from loguru import logger
from fastapi import Request
from src.utils.settings import BASE_DIR


def get_logger(path: str):
    log_path = BASE_DIR / path
    format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{"
        "function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    # TODO add LOGGER_LEVEL in .env and configure it in settings
    logger.remove()
    logger.add(
        log_path,
        format=format,
        level="DEBUG",
        rotation="1 week",
        compression="zip",
    )
    logger.add(stdout, level="DEBUG", format=format, colorize=True)
    return logger


async def logging_dependency(request: Request):
    """Simple class for logging each request"""

    logger.debug(f"{request.method} {request.url}")
    logger.debug("Params:")
    for name, value in request.path_params.items():
        logger.debug(f"\t{name}: {value}")
    logger.debug("Headers:")
    for name, value in request.headers.items():
        logger.debug(f"\t{name}: {value}")
