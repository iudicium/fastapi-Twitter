from fastapi import FastAPI, Depends
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from starlette.exceptions import HTTPException
from uvicorn import run
from loguru import logger
from src.routes import media_route, user_route, tweet_route
from src.database.utils import init_models
from src.utils.loggerconf import get_logger, logging_dependency
from src.utils.settings import get_server_settings
from src.utils.exceptions import (
    validation_exception_handler,
    custom_http_exception_handler,
    response_validation_exception_handler,
)


# Need to remove the file
get_logger("logs/logs.log")
app = FastAPI(debug=True)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, custom_http_exception_handler)
app.add_exception_handler(
    ResponseValidationError, response_validation_exception_handler
)

app.include_router(media_route.router, dependencies=[Depends(logging_dependency)])
app.include_router(user_route.router, dependencies=[Depends(logging_dependency)])
app.include_router(tweet_route.router, dependencies=[Depends(logging_dependency)])


@app.on_event("startup")
async def create_initial_data():
    logger.info("Creating initial tables")
    await init_models()


if __name__ == "__main__":
    settings = get_server_settings()

    run(app, host=settings.HOST, port=int(settings.PORT))
