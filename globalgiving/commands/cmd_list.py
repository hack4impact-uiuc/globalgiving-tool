import click
from globalgiving.cli import pass_context, authenticate
from globalgiving.db import list_scrapers_from_db
import os


@click.command("list", short_help="List all available scrapers.")
@pass_context
def cli(ctx):
    authenticate()
    """
    GG list lists all scrapers registered on the database. It prints out each
    name and all routes associated with that scraper.
    """
    ctx.log("Listing all registered scrapers!")
    ctx.log(os.path.realpath(os.path.dirname(__file__)+"/.."))
    all_docs = list_scrapers_from_db()
    for doc in all_docs:
        ctx.log("  {}".format(doc["name"]))
    return all_docs  # for testing
