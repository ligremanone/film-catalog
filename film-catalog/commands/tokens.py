from random import choice
from typing import Annotated

import typer
from rich import print
from rich.markdown import Markdown

from api.api_v1.auth.services import redis_tokens

app = typer.Typer(
    name="tokens",
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Tokens management",
)
RANDOM_EMOJI = [
    ":smiley:",
    ":vampire:",
    ":pile_of_poo:",
    ":thumbs_up:",
    ":raccoon:",
    ":cucumber:",
    ":hankey:",
]


@app.command(help="Check if the passed token is valid - exists or not")
def check(token: Annotated[str, typer.Argument(help="Token to check")]) -> None:
    print(
        f"Token [yellow bold]{token}",
        (
            "[green]exists :cucumber:"
            if redis_tokens.token_exists(token)
            else "[red]does not exist :hankey:"
        ),
    )


@app.command(
    help="List all tokens",
    name="list",
)
def list_tokens() -> None:
    print(Markdown("""# This is all valid tokens:"""))
    for token in redis_tokens.get_tokens():
        print(f"{choice(RANDOM_EMOJI)} [green bold]{token}")


@app.command(
    help="Delete token",
    name="rm",
)
def delete_token(
    token: Annotated[str, typer.Argument(help="Token to delete")],
) -> None:
    if not redis_tokens.token_exists(token):
        print(f"Token [yellow]{token}[/] [red]does not exist :hankey:")
        return
    redis_tokens.delete_token(token)
    print(f"Token [bold green]{token}[/] [red]deleted[/] from db")


@app.command(
    help="Generate and save token",
    name="create",
)
def create_and_save_token() -> None:
    new_token = redis_tokens.generate_and_save_token()
    print(
        f"Token [bold medium_purple1]{new_token}[/] generated and saved to db :smiley:",
    )


@app.command(
    help="Add token",
    name="add",
)
def add_token(
    token: Annotated[str, typer.Argument(help="New token")],
) -> None:
    redis_tokens.add_token(token)
    print(f"Token [bold medium_purple1]{token}[/] added to db")
