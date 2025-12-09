from typing import Any, TypedDict

from fastapi import Request

FLASHED_MESSAGES_KEY = "_flash_messages"


class Message(TypedDict):
    message: str
    category: str


def flash(
    request: Request,
    message: str,
    category: str = "info",
) -> None:
    if FLASHED_MESSAGES_KEY not in request.session:
        request.session[FLASHED_MESSAGES_KEY] = []
    request.session[FLASHED_MESSAGES_KEY].append(
        Message(message=message, category=category),
    )


def get_flash_messages(request: Request) -> Any | list[Message]:  # noqa: ANN401
    return request.session.pop(FLASHED_MESSAGES_KEY, [])
