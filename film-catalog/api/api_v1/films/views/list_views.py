from fastapi import APIRouter, status, BackgroundTasks
from api.api_v1.films.crud import storage
from schemas.film import Film, FilmCreate, FilmRead

router = APIRouter(
    prefix="/films",
    tags=["films"],
)


@router.get(
    "/",
    response_model=list[FilmRead],
)
async def get_all_films():
    return storage.get()


@router.post(
    "/",
    response_model=Film,
    status_code=status.HTTP_201_CREATED,
)
async def create_film(
    new_film: FilmCreate,
    background_tasks: BackgroundTasks,
):
    background_tasks.add_task(storage.save_data)
    return storage.create(new_film)
