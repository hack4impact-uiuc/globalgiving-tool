import click, requests
from globalgiving.db import list_from_db
from globalgiving.cli import pass_context, authenticate


@click.command("urls", short_help="Lists all the urls with scrapers")
@click.argument("n", required=True, type=str)
@pass_context
def cli(ctx, n):
    authenticate()
    search = "Finding scraper {} from list of registered scrapers..."
    scrapers = list_from_db()
    routes = list(
        map(lambda scraper: scraper["routes"]["Test"][0:-4] + "url", scrapers)
    )
    for route in routes:
        print(route)
        contents = requests.get(route).text
        print(contents)
