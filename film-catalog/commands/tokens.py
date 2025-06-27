from typing import Annotated
from random import choice
import typer
from rich import print
from api.api_v1.auth.services import redis_tokens
from rich.console import Console
from rich.markdown import Markdown

app = typer.Typer(
    name="tokens",
    no_args_is_help=True,
    rich_markup_mode="rich",
    help="Tokens management",
)
console = Console()
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


@app.command(help="Get all tokens")
def list():
    console.print(Markdown("""# This is all valid tokens:"""))
    for token in redis_tokens.get_tokens():
        print(f"{choice(RANDOM_EMOJI)} [green bold]{token}")
