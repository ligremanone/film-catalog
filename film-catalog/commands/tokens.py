from typing import Annotated

import typer
from rich import print
from api.api_v1.auth.services import redis_tokens

app = typer.Typer(
    name="tokens",
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Tokens management",
)


@app.command(help="Check if the passed token is valid - exists or not")
def check(token: Annotated[str, typer.Argument(help="Token to check")]):
    print(
        f"Token [yellow bold]{token}",
        (
            "[green]exists :cucumber:"
            if redis_tokens.token_exists(token)
            else "[red]does not exist :hankey:"
        ),
    )
