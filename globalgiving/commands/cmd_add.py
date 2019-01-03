import click
import requests
from globalgiving.cli import pass_context, authenticate
from globalgiving.db import db_get_collection, send_scraper_to_db


@click.command("add", short_help="Add a new scraper or update an existing one.")
@click.argument("name", required=True)
@click.argument("url", required=True)
@pass_context
def cli(ctx, name, url):
    """
    Registers the given scraper with the database. It basically just gets all
    possible routes from the `/routes` route then sets up appropriate inputs
    for gg.db.send_scraper_to_db().
    """
    authenticate()
    collection = db_get_collection()
    result = send_scraper_to_db(collection, name, url)
    ctx.log(result)


def dev_add(collection, name, url):
    """
    This function is to be used for testing; it mirrors the code above, but
    does not use click and allows a mocked DB to be passed in.
    """
    result = send_scraper_to_db(collection, name, url, test=True)
    return str(result)
