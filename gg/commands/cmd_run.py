import click, requests
from gg.db import list_from_db
from gg.cli import pass_context


@click.command("run", short_help="Run a scraper")
@click.option("--n", nargs=1, required=True, type=str)
@pass_context
def cli(ctx, n):
    search = "Finding scraper {} from list of registered scrapers..."
    ctx.log(search.format(n))

    try:
        scraper = next(filter(lambda scraper: scraper["name"] == n, list_from_db()))
        ctx.log("Scraper {} found!".format(n))
    except StopIteration:
        ctx.log("Scraper {} not found.".format(n))
        return

    contents = requests.get(scraper["routes"]["Routes"]).text
    ctx.log(contents)
