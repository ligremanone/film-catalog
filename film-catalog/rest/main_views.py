from typing import Any

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from templating import templates

router = APIRouter(include_in_schema=False)


@router.get(
    "/",
    name="home",
)
async def home_page(request: Request) -> HTMLResponse:
    context: dict[str, Any] = {}
    features = [
        "Movie Catalog",
        "Advanced Search & Filters",
        "Movie Pages",
        "Recommendations",
    ]
    context.update(
        features=features,
    )
    return templates.TemplateResponse(
        request,
        "home.html",
        context=context,
    )


@router.get(
    "/about/",
    name="about",
)
async def about_page(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "about.html",
    )
