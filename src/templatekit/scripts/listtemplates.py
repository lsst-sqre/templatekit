"""Subcommand for listing available file or project templates."""

from __future__ import annotations

__all__ = ("list_templates",)


import click

from ..repo import Repo


@click.command()
@click.option(
    "-t",
    "--type",
    "template_type",
    type=click.Choice(["all", "file", "project"]),
    default="all",
    help="The type of templates to show. File templates are single files or "
    "snippets. Project templates create whole project directories.",
)
@click.pass_obj
def list_templates(state: dict[str, Repo], template_type: str) -> None:
    """List available templates in the repository."""
    repo = state["repo"]

    if template_type in ("all", "file"):
        click.echo(click.style("File templates:", bold=True))
        for file_template in repo.iter_file_templates():
            click.echo(f"    {file_template.name}")

    if template_type in ("all", "project"):
        click.echo(click.style("Project templates:", bold=True))
        for project_template in repo.iter_project_templates():
            click.echo(f"    {project_template.name}")
