from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

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
        try:
            film_in = FilmUpdate.model_validate(film_form)
        except ValidationError as err:
            return form_response.render(
                request=request,
                form_data=film_form,
                pydantic_error=err,
                form_validated=True,
                film=film,
            )
    storage.update(film, film_in)
    return RedirectResponse(
        url=request.url_for("films:list"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
