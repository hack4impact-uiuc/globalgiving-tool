import click
import requests
from gg.db import list_from_db, upload_data
from gg.cli import pass_context


@click.command("run", short_help="Run a scraper")
@click.argument("name", required=True, type=str)
@pass_context
def cli(ctx, name):
    search = "Finding scraper {} from list of registered scrapers..."
    ctx.log(search.format(name))
    try:
        scrapers = list_from_db()
        route = list(filter(lambda scraper: scraper["name"] == str(name), scrapers))[0][
            "routes"
        ]["Data"]
        ctx.log("Scraper {} found!".format(name))
    except StopIteration:
        ctx.log("Scraper {} not found.".format(name))
        return
    contents = requests.get(route).json()
    result = upload_data(contents)
    ctx.log(result)
