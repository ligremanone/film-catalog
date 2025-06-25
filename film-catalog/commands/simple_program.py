import typer
from rich import print
import art

app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
)


@app.command(help="Just a [bold red]simple[/] program")
def simple_program():
    print(
        art.text2art(
            "Hello World!",
            "rand",
        )
    )
    print(f'[green]{art.art("coffee")}')
