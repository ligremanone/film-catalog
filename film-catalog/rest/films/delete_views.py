from fastapi import APIRouter, status
from fastapi.responses import Response

from dependencies.films import FilmBySlug, GetFilmsStorage

router = APIRouter(prefix="/{slug}/delete")


@router.delete("/", name="film:delete")
def delete_film(
    storage: GetFilmsStorage,
    film: FilmBySlug,
) -> Response:
    storage.delete(film)
    return Response(
        status_code=status.HTTP_200_OK,
        content="",
    )
