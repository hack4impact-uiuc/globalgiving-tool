import click
from globalgiving.cli import pass_context, authenticate
from globalgiving.db import list_scrapers_from_db


@click.command("routes", short_help="List all available scrapers.")
@click.argument("name", required=True, type=str)
@pass_context
def cli(ctx, name):
    """
    GG list lists all scrapers registered on the database. It prints out each
    name and all routes associated with that scraper.
    """
    authenticate()
    all_docs = list_scrapers_from_db()
    for doc in all_docs:
        if doc["name"] == name:
            ctx.log("Name: {}".format(doc["name"]))
            for route in doc["routes"].keys():
                if route != "Routes":
                    ctx.log("    {}: {}".format(route, doc["routes"][route]))
