import click
import os
from cookiecutter.main import cookiecutter

from globalgiving.cli import pass_context
from globalgiving.db import list_scrapers_from_db


MS_DIR = "/microservices"
TEMP_DIR = "/cookiecutter-scraper"
MS_DELIM = "_" # Delimeter to split on to check microservice existence
TEMP_NAME_PARAM = "project_slug" # Slug placeholder to be replaced by inputted name


@click.command("generate", short_help="Generate a new scraper template")
@click.argument("name", required=True, type=str)
@pass_context
def cli(ctx, name):
    """
    GG generate creates a new template scraper from the template in the microservices directory
    and using the cookiecutter module.
    """
    # Get root directory and set start of existing scraper search to the root microservices directory
    rootdir = os.pardir + MS_DIR
    subdir_list = next(os.walk(rootdir))[1]

    # Check if scraper already exists in list of subdirectories
    for scraper in subdir_list:
        name_start_idx = scraper.find(MS_DELIM)
        if name == scraper[name_start_idx + 1 :]:
            ctx.log("Scraper {} already exists!".format(name))
            return

    # If scraper doesn't already exist, create new scraper template with the passed in name
    cookiecutter(
        rootdir + TEMP_DIR,
        extra_context={TEMP_NAME_PARAM: name},
        no_input=True,
        output_dir=rootdir,
    )
    ctx.log("Scraper {} successfully created!".format(name))
