import click
from gg.cli import pass_context
from gg.db import list_from_db


@click.command("list", short_help="List all available scrapers.")
@pass_context
def cli(ctx):
    """
    GG list lists all scrapers registered on the database. It prints out each
    name and all routes associated with that scraper.
    """
    ctx.log("Listing all registered scrapers!")
    all_docs = list_from_db()
    for doc in all_docs:
        ctx.log("\nName: {}".format(doc["name"]))
        ctx.log("Available Routes for {}:".format(doc["_id"]))
        for route in doc["routes"].keys():
            if route != "Routes":
                ctx.log("    {}: {}".format(route, doc["routes"][route]))
    return all_docs  # for testing
