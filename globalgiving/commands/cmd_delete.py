import click
from globalgiving.db import db_get_collection, list_scrapers_from_db, delete_scraper
from globalgiving.cli import pass_context, authenticate


@click.command("delete", short_help="Delete a scraper's registration.")
@click.argument("name", required=True, type=str)
@pass_context
def cli(ctx, name):
    authenticate()
    collection = db_get_collection()
    search = "Finding scraper {} from list of registered scrapers . . . "
    ctx.log(search.format(name))
    try:
        scrapers = list_scrapers_from_db(collection)
        ngo_id = list(filter(lambda scraper: scraper["name"] == str(name), scrapers))[
            0
        ]["_id"]
        ctx.log("Scraper {} found!".format(name))
    except StopIteration:
        ctx.log("Scraper {} not found.".format(name))
        return
    except IndexError:
        ctx.log("Scraper {} not found.".format(name))
        return
    ctx.log("Deleting scraper {} . . . ".format(name))
    return delete_scraper(collection, ngo_id)
