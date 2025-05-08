from fastapi import APIRouter
from .films.views import router as films_router

router = APIRouter(prefix="/v1")
router.include_router(films_router)
