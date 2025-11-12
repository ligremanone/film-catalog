from fastapi import APIRouter

from rest.films import router as films_router
from rest.main_views import router as main_view_router

router = APIRouter()
router.include_router(main_view_router)
router.include_router(films_router)
