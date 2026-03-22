"""LinkCtl CLI — stub for workflow-pipeline E2E testing."""

import click


@click.group()
def main():
    """LinkCtl — a simple link shortener."""
    pass


@main.command()
def version():
    """Show version."""
    click.echo("linkctl 0.1.0")
