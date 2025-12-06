from typing import Any

from pydantic import BaseModel, ValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import HTMLResponse

from templating import templates


class FormResponseHelper:
    def __init__(
        self,
        model: type[BaseModel],
        template_name: str,
    ) -> None:
        self.model = model
        self.template_name = template_name

    @classmethod
    def format_pydantic_errors(cls, error: ValidationError) -> dict[str, str]:
        return {f'{e["loc"][0]}': e["msg"] for e in error.errors()}

    def render(
        self,
        request: Request,
        form_data: Any = None,  # noqa: ANN401
        form_validated: bool = False,  # noqa: FBT002 FBT001
        errors: dict[str, str] | None = None,
        pydantic_error: ValidationError | None = None,
        **context_extra: Any,  # noqa: ANN401
    ) -> HTMLResponse:
        if pydantic_error:
            errors = self.format_pydantic_errors(pydantic_error)
        context: dict[str, Any] = {}
        model_schema = self.model.model_json_schema()
        context.update(
            model_schema=model_schema,
            errors=errors,
            form_validated=form_validated,
            form_data=form_data,
        )
        context.update(context_extra)
        return templates.TemplateResponse(
            request=request,
            name=self.template_name,
            context=context,
            status_code=(
                status.HTTP_422_UNPROCESSABLE_ENTITY
                if form_validated and errors
                else status.HTTP_200_OK
            ),
        )
