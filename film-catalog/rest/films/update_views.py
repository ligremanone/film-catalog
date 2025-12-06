from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse

from dependencies.films import FilmBySlug, GetFilmsStorage
from schemas.film import FilmUpdate
from services.films import FormResponseHelper

router = APIRouter(prefix="/{slug}/update")

form_response = FormResponseHelper(model=FilmUpdate, template_name="films/update.html")


@router.get("/", name="film:update-view")
def get_page_update_film(
    request: Request,
    film: FilmBySlug,
) -> HTMLResponse:
    form = FilmUpdate(**film.model_dump())
    return form_response.render(
        request,
        form_data=form,
        film=film,
    )


@router.post("/", name="film:update", response_model=None)
async def create_film(
    request: Request,
    storage: GetFilmsStorage,
    film: FilmBySlug,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as film_form:
        film_from_form = FilmUpdate.model_validate(film_form)
    storage.update(film, film_from_form)
    return RedirectResponse(
        url=request.url_for("films:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
