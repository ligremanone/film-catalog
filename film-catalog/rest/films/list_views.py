from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, Request
from starlette.responses import HTMLResponse

from dependencies.films import GetFilmsStorage
from templating import templates

if TYPE_CHECKING:
    from schemas.film import Film
router = APIRouter()


@router.get(
    "/",
    name="films:list",
    response_class=HTMLResponse,
)
def list_view(
    request: Request,
    storage: GetFilmsStorage,
) -> HTMLResponse:
    context: dict[str, Any] = {}
    films: list[Film] = storage.get()
    context.update(films=films)
    return templates.TemplateResponse(
        request,
        "films/list.html",
        context=context,
    )
