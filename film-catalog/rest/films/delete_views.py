from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse

from dependencies.films import FilmBySlug, GetFilmsStorage

router = APIRouter(prefix="/{slug}/delete")


@router.post("/", name="film:delete")
def delete_film(
    request: Request,
    storage: GetFilmsStorage,
    film: FilmBySlug,
) -> RedirectResponse:
    storage.delete(film)
    return RedirectResponse(
        url=request.url_for("films:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
