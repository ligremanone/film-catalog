from typing import Any

from fastapi import APIRouter, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import ValidationError

from dependencies.films import GetFilmsStorage
from schemas.film import FilmCreate
from services.films import FormResponseHelper
from storage.films.exceptions import FilmAlreadyExistsError
from templating import templates
from utils.flash_messages import flash

router = APIRouter(prefix="/create")

form_response = FormResponseHelper(model=FilmCreate, template_name="films/create.html")


def create_view_validation_response(
    request: Request,
    form_data: Any = None,  # noqa: ANN401
    errors: dict[str, str] | None = None,
    form_validated: bool = True,  # noqa: FBT001, FBT002
) -> HTMLResponse:
    context: dict[str, Any] = {}
    model_schema = FilmCreate.model_json_schema()
    context.update(
        model_schema=model_schema,
        errors=errors,
        form_validated=form_validated,
        form_data=form_data,
    )
    return templates.TemplateResponse(
        request=request,
        name="films/create.html",
        context=context,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def format_pydantic_errors(error: ValidationError) -> dict[str, str]:
    return {f'{e["loc"][0]}': e["msg"] for e in error.errors()}


@router.get("/", name="film:create-view")
def get_page_create_film(request: Request) -> HTMLResponse:
    return form_response.render(request)


@router.post("/", name="film:create", response_model=None)
async def create_film(
    request: Request,
    storage: GetFilmsStorage,
) -> RedirectResponse | HTMLResponse:
    async with request.form() as film_form:
        try:
            new_film = FilmCreate.model_validate(film_form)
        except ValidationError as err:
            return form_response.render(
                request=request,
                form_data=film_form,
                pydantic_error=err,
                form_validated=True,
            )
    try:
        storage.create_or_raise_if_exists(new_film)
    except FilmAlreadyExistsError:
        errors = {"slug": f"Film with slug {new_film.slug!r} already exists"}
    else:
        flash(
            request=request,
            message=f"Successfully created film {new_film.slug!r}",
            category="success",
        )
        return RedirectResponse(
            url=request.url_for("films:list"),
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return form_response.render(
        request=request,
        form_data=new_film,
        errors=errors,
        form_validated=True,
    )
