import click, requests
from globalgiving.db import list_from_db
from globalgiving.cli import pass_context, authenticate


@click.command("urls", short_help="Lists all the urls with scrapers")
@pass_context
def cli(ctx):
    authenticate()
    search = "Finding scraper {} from list of registered scrapers..."
    scrapers = list_from_db()
    for scraper in scrapers:
        print("Scraper: " + scraper["name"])
        contents = requests.get(scraper["routes"]["Test"][0:-4] + "url").text
        if "http" in contents:
            print("       " + contents)
        else:
            print("       ERROR: Scraper not avalible")
