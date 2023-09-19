from contextlib import asynccontextmanager
from datetime import datetime
from platform import python_version, release, system

from fastapi import Depends, FastAPI
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from loguru import logger
from starlette.exceptions import HTTPException
from uvicorn import run

from src.database.database import engine
from src.routes import media_route, tweet_route, user_route
from src.utils.exceptions import (
    custom_http_exception_handler,
    response_validation_exception_handler,
    validation_exception_handler,
)
from src.utils.loggerconf import get_logger, logging_dependency
from src.utils.settings import get_server_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup_time = datetime.now()
    logger.info(f"Python Version: {python_version()}")
    logger.info(f"Operating System: {system()} {release()}")
    logger.info(f"Server is starting up at {startup_time}")
    logger.info(f"Debug Mode: {settings.DEBUG}")
    logger.info(f"Produciton: {settings.PRODUCTION}")
    logger.info(f"Server is starting up on {settings.HOST}:{settings.PORT}")
    yield
    logger.info("Performing shutdown.")
    total_running_time = datetime.now() - startup_time
    logger.info(f"Server has been running for {total_running_time}")
    logger.info("Closing all connections from engine pool")
    await engine.dispose()


settings = get_server_settings()
get_logger()

app = FastAPI(
    title="Twitter",
    description="Simple Twitter FASTAPI",
    debug=settings.DEBUG,
    lifespan=lifespan,
    docs_url="/docs" if not settings.PRODUCTION else None,
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(
    ResponseValidationError, response_validation_exception_handler
)

app.include_router(media_route.router, dependencies=[Depends(logging_dependency)])
app.include_router(user_route.router, dependencies=[Depends(logging_dependency)])
app.include_router(tweet_route.router, dependencies=[Depends(logging_dependency)])


if __name__ == "__main__":
    run(app, host=settings.HOST, port=int(settings.PORT))
