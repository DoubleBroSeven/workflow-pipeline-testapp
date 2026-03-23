"""LinkCtl CLI — command-line interface for the link shortener."""

import click
import uvicorn


@click.group()
def main():
    """LinkCtl — a simple link shortener."""
    pass


@main.command()
def version():
    """Show version."""
    click.echo("linkctl 0.1.0")


@main.command()
@click.option("--host", default="127.0.0.1", help="Host to bind to.")
@click.option("--port", default=8000, type=int, help="Port to bind to.")
def serve(host: str, port: int):
    """Start the LinkCtl server."""
    from linkctl.server import create_app

    app = create_app()
    uvicorn.run(app, host=host, port=port)
