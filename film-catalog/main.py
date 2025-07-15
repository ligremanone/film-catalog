import logging

from fastapi import FastAPI

from api import router as api_router
from api.main_views import router as main_router
from app_lifespan import lifespan
from core.config import LOG_FORMAT, LOG_LEVEL

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT,
)
app = FastAPI(
    name="Film Catalog",
    title="Film Catalog",
    lifespan=lifespan,
)
app.include_router(api_router)
app.include_router(main_router)
