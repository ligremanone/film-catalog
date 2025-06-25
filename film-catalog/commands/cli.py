__all__ = [
    "app",
]
import typer
from .simple_program import app as simple_app

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)
app.add_typer(simple_app)


@app.callback()
def callback():
    """
    Some CLI management commands
    """
