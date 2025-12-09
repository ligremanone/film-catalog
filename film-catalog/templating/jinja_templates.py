from datetime import UTC, date, datetime

from fastapi import Request
from fastapi.templating import Jinja2Templates

from core.config import BASE_DIR
from utils.flash_messages import get_flash_messages


def inject_current_date(request: Request) -> dict[str, date]:  # noqa: ARG001
    now = datetime.now(tz=UTC)
    return {
        "today": now.today(),
        "now": now,
    }


templates = Jinja2Templates(
    directory=BASE_DIR / "templates",
    context_processors=[inject_current_date],
)
templates.env.globals["get_flash_messages"] = get_flash_messages
