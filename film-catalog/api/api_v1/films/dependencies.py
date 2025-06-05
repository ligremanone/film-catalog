import logging
from typing import Annotated

from fastapi import HTTPException, status, BackgroundTasks, Request, Query, Header
from fastapi.params import Depends
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
    HTTPBasic,
    HTTPBasicCredentials,
)
from api.api_v1.films.crud import storage
from core.config import API_TOKENS, USER_DB
from schemas.film import Film

log = logging.getLogger(__name__)

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    }
)
static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your API token for developer portal",
    auto_error=False,
)
user_basic_auth = HTTPBasic(
    scheme_name="User Basic Auth",
    description="Basic username and password auth",
    auto_error=False,
)


async def prefetch_film(slug: str) -> Film:
    film = storage.get_by_slug(slug)
    if film:
        return film

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Film with {slug!r} slug not found",
    )


def save_storage_data(
    background_tasks: BackgroundTasks,
    request: Request,
):
    yield
    if request.method not in UNSAFE_METHODS:
        return
    log.info("Add background task to save data")
    background_tasks.add_task(storage.save_data)


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
):
    if api_token.credentials not in API_TOKENS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API token",
        )


def check_api_token_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token required",
        )
    validate_api_token(api_token)


def validate_basic_auth(
    credentials: HTTPBasicCredentials | None,
):
    if (
        credentials
        and credentials.username in USER_DB
        and credentials.password == USER_DB[credentials.username]
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None, Depends(user_basic_auth)
    ] = None,
):
    log.info("User credentials %s", credentials)
    if request.method not in UNSAFE_METHODS:
        return
    validate_basic_auth(credentials)


def api_token_or_user_basic_auth_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None, Depends(user_basic_auth)
    ] = None,
):
    if request.method not in UNSAFE_METHODS:
        return None
    if credentials:
        return validate_basic_auth(credentials)
    if api_token:
        return validate_api_token(api_token)
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="API token or user credentials required",
    )
