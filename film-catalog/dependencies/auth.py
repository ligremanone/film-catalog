import logging
from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from starlette.requests import Request

from services.auth import redis_users

UNSAFE_METHODS = frozenset(
    {
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
    },
)
user_basic_auth = HTTPBasic(
    scheme_name="User Basic Auth",
    description="Basic username and password auth",
    auto_error=False,
)
log = logging.getLogger(__name__)


def validate_basic_auth(
    credentials: HTTPBasicCredentials | None,
) -> None:
    if credentials and redis_users.validate_user_password(
        credentials.username,
        credentials.password,
    ):
        return
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User credentials required. Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )


def user_basic_auth_required_for_unsafe_methods(
    request: Request,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
) -> None:
    log.info("User credentials %s", credentials)
    if request.method not in UNSAFE_METHODS:
        return
    validate_basic_auth(credentials)
