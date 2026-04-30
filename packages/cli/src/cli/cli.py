"""CLI using Typer."""

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

@app.callback()
def welcome():
    """Print a welcome message to the user."""
    print("Welcome!")

if __name__ == "__main__":
    app()
