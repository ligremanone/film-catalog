from typing import Annotated
from random import choice
import typer
from rich import print
from api.api_v1.auth.services import redis_tokens
from rich.markdown import Markdown

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
def check(token: Annotated[str, typer.Argument(help="Token to check")]):
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
def list_tokens():
    print(Markdown("""# This is all valid tokens:"""))
    for token in redis_tokens.get_tokens():
        print(f"{choice(RANDOM_EMOJI)} [green bold]{token}")


@app.command(
    help="Delete token",
    name="rm",
)
def delete_token(
    token: Annotated[str, typer.Argument(help="Token to delete")],
):
    redis_tokens.delete_token(token)


@app.command(
    help="Generate and save token",
    name="create",
)
def create_and_save_token():
    redis_tokens.generate_and_save_token()


@app.command(
    help="Add token",
    name="add",
)
def add_token(
    token: Annotated[str, typer.Argument(help="New token")],
):
    redis_tokens.add_token(token)
