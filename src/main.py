from fastapi import FastAPI
from uvicorn import run

from src.routes import media_route, user_route
from src.database.utils import init_models
from src.utils.loggerconf import get_logger
from src.utils.settings import get_server_settings

app = FastAPI(debug=True)

app.include_router(media_route.router)
app.include_router(user_route.router)


@app.on_event("startup")
async def create_initial_data():
    logger.info("Creating initial tables")
    await init_models()


if __name__ == "__main__":
    settings = get_server_settings()
    logger = get_logger("logs/logs.log")
    run(app, host="localhost", port=8000)
