import click
from globalgiving.cli import pass_context, authenticate
from globalgiving.db import db_get_collection, list_scrapers_from_db


@click.command("list", short_help="List all available scrapers.")
@pass_context
def cli(ctx):
    authenticate()
    """
    GG list lists all scrapers registered on the database. It prints out each
    name and all routes associated with that scraper.
    """
    collection = db_get_collection()
    ctx.log("Listing all registered scrapers!")
    all_docs = list_scrapers_from_db(collection)
    for doc in all_docs:
        ctx.log("  {}".format(doc["name"]))
    return all_docs  # for testing
