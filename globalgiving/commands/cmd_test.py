import click
import requests
from globalgiving.db import db_get_collection, list_scrapers_from_db
from globalgiving.cli import pass_context, authenticate
from globalgiving.config import SCRAPER_COLL_NAME_FIELD


@click.command("test", short_help="Test a scraper")
@click.argument("n", required=True, type=str)
@pass_context
def cli(ctx, n):
    authenticate()
    collection = db_get_collection()
    search = "Finding scraper {} from list of registered scrapers..."
    ctx.log(search.format(n))
    try:
        scrapers = list_scrapers_from_db(collection)
        scraper = list(filter(lambda scraper: scraper[SCRAPER_COLL_NAME_FIELD] == n, scrapers))
        route = scraper[0]["_id"] + "/test"
        ctx.log("Scraper {} found!".format(n))
    except Exception:
        ctx.log("Scraper {} not found.".format(n))
        return
    contents = requests.get(route).text
    print(contents)


def dev_testscraper(collection, name):
    try:
        scrapers = list_scrapers_from_db(collection)
        scraper = list(filter(lambda scraper: scraper[SCRAPER_COLL_NAME_FIELD] == n, scrapers))
        route = scraper[0]["_id"] + "/test"
    except Exception:
        return
    return requests.get(route).text
