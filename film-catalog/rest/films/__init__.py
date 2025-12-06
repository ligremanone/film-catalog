from fastapi import APIRouter, Depends

from dependencies.auth import user_basic_auth_required_for_unsafe_methods
from rest.films.create_views import router as create_views_router
from rest.films.list_views import router as list_views_router
from rest.films.update_views import router as update_views_router

router = APIRouter(
    tags=["Films REST"],
    prefix="/films",
    dependencies=[
        Depends(user_basic_auth_required_for_unsafe_methods),
    ],
)
router.include_router(list_views_router)
router.include_router(create_views_router)
router.include_router(update_views_router)
