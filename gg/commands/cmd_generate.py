import click
from gg.cli import pass_context
from gg.db import list_from_db
import os
import subprocess


@click.command("generate", short_help="Generate a new scraper template")
@pass_context
def cli(ctx):
    """
    GG list lists all scrapers registered on the database. It prints out each
    name and all routes associated with that scraper.
    """
    p = subprocess.Popen(["cookiecutter","--no-input" ,"."], cwd=str(os.path.dirname(os.path.realpath(__file__)))[:-11] + "microservices")
    p.wait()

    

