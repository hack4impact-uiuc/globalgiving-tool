import click
import os
from cookiecutter.main import cookiecutter

from globalgiving.cli import pass_context
from globalgiving.db import list_scrapers_from_db


MICROSERVICES_DIRECTORY = "/microservices"
COOKIE_CUTTER_DIRECTORY = "/cookiecutter-scraper"


@click.command("generate", short_help="Generate a new scraper template")
@click.argument("name", required=True, type=str)
@pass_context
def cli(ctx, name):
    """
    GG generate creates a new template scraper from the template in the microservices directory
    and using the cookiecutter module.
    """
    # Get root directory and set start of existing scraper search to the root microservices directory
    rootdir = os.pardir + MICROSERVICES_DIRECTORY
    subdir_list = next(os.walk(rootdir))[1]

    # Check if scraper already exists in list of subdirectories
    for scraper in subdir_list:
        name_start_idx = scraper.find("_")
        if name == scraper[name_start_idx + 1 :]:
            ctx.log("Scraper {} already exists!".format(name))
            return

    # If scraper doesn't already exist, create new scraper template with the passed in name
    cookiecutter(
        rootdir + COOKIE_CUTTER_DIRECTORY,
        extra_context={"project_slug": name},
        no_input=True,
        output_dir=rootdir,
    )
    ctx.log("Scraper {} successfully created!".format(name))
