import logging

from fastapi import FastAPI

from api import router as api_router
from api.main_views import router as main_router
from app_lifespan import lifespan
from core.config import settings

logging.basicConfig(
    level=settings.logging.log_level,
    format=settings.logging.log_format,
    datefmt=settings.logging.date_format,
)
app = FastAPI(
    name="Film Catalog",
    title="Film Catalog",
    lifespan=lifespan,
)
app.include_router(api_router)
app.include_router(main_router)
