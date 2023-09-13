from loguru import logger as logg_conf

from src.utils.settings import BASE_DIR


def get_logger(path: str):
    log_path = BASE_DIR / path
    # TODO add LOGGER_LEVEL in .env and configure it in settings
    logg_conf.add(
        log_path,
        format="{time:YYYY-MM-DD HH:mm:ss} {level: <8} {process} --- {line: <8} [{name}] {function: <24} : {message}",
        level="INFO",
        rotation="1 week",
        compression="zip",
    )

    return logg_conf
