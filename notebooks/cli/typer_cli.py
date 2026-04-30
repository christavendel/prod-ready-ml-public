"""CLI using Typer."""

from typing import Annotated
import typer

app = typer.Typer(
    name="CLI using Typer"
)

@app.command()
def say_hi(name):
    """Say hello to the user."""
    typer.echo(f"Hello: {name}")

@app.command()
def goodbye():
    """Say goodbye to the user."""
    typer.echo("Goodbye!")

@app.command()
def greet(name):
    """Greet a person by name."""
    typer.echo(f"Greetings, {name}!")

@app.command()
def welcome(name: str, greeting: str = "Hello", enthusiastic : Annotated[bool, typer.Option("--enthusiastic")] = False):
    """Custom greeting of a person."""
    if enthusiastic:
        typer.echo(f"{greeting} {name}!!!")
    else:

        typer.echo(f"{greeting} {name}")

if __name__ == "__main__":
    app()
