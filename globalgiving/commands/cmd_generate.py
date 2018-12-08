import click
import os
import os
from cookiecutter.main import cookiecutter

from globalgiving.cli import pass_context
from globalgiving.db import list_scrapers_from_db


@click.command("generate", short_help="Generate a new scraper template")
@click.argument("name", required=True, type=str)
@pass_context
def cli(ctx, name):
    """
    GG generate creates a new template scraper
    """
    # Get root directory set start of scraper search to the root microservices directory
    rootdir = os.getcwd() + "/microservices"
    subdir_list = next(os.walk(rootdir))[1]

    # Check if scraper already exists in list of subdirectories
    for scraper in subdir_list:
        name_start_idx = scraper.find("-")
        if name == scraper[name_start_idx + 1 :]:
            ctx.log("Scraper {} already exists!".format(name))
            return

    # If scraper doesn't already exist, create new scraper template with the passed in name
    cookiecutter(
        rootdir + "/cookiecutter-scraper",
        extra_context={"project_slug": name},
        no_input=True,
        output_dir=rootdir,
    )
    ctx.log("Scraper {} successfully created!".format(name))
