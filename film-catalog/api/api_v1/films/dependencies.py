import logging
from typing import Annotated

from fastapi import HTTPException, Request, status
from fastapi.params import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBasicCredentials,
    HTTPBearer,
)

from dependencies.auth import UNSAFE_METHODS, user_basic_auth, validate_basic_auth
from services.auth import redis_tokens

log = logging.getLogger(__name__)


static_api_token = HTTPBearer(
    scheme_name="Static API token",
    description="Your API token for developer portal",
    auto_error=False,
)


def validate_api_token(
    api_token: HTTPAuthorizationCredentials,
) -> None:
    if redis_tokens.token_exists(api_token.credentials):
        return
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
) -> None:
    if request.method not in UNSAFE_METHODS:
        return
    if not api_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API token required",
        )
    validate_api_token(api_token)


def api_token_or_user_basic_auth_required_for_unsafe_methods(
    request: Request,
    api_token: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(static_api_token),
    ] = None,
    credentials: Annotated[
        HTTPBasicCredentials | None,
        Depends(user_basic_auth),
    ] = None,
) -> None:
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
