import click
from globalgiving.cli import pass_context, authenticate
from globalgiving.db import db_get_collection, list_scrapers_from_db
from globalgiving.config import SCRAPER_COLL_NAME_FIELD


@click.command("list", short_help="List all available scrapers.")
@pass_context
def cli(ctx):
    """
    GG list lists all scrapers registered on the database. It prints out each
    name and all routes associated with that scraper.
    """
    authenticate()
    collection = db_get_collection()
    ctx.log("Listing all registered scrapers!")
    all_docs = list_scrapers_from_db(collection)
    for doc in all_docs:
        ctx.log("  {}".format(doc[SCRAPER_COLL_NAME_FIELD]))


def dev_list(collection):
    """
    Helper method that gets called when testing the command using a mocked collection.

    Input:
        collection: collection to perform operations with/on
    """
    all_docs = list_scrapers_from_db(collection)
    return all_docs
