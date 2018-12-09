import click
import requests
from globalgiving.db import list_scrapers_from_db
from globalgiving.cli import pass_context, authenticate


@click.command("urls", short_help="Lists all the urls with scrapers")
@pass_context
def cli(ctx):
    authenticate()
    scrapers = list_scrapers_from_db()
    for scraper in scrapers:
        print("Scraper: " + scraper["name"])
        contents = requests.get(scraper["routes"]["Test"][0:-4] + "url").text
        if "http" in contents:
            print("       " + contents)
        else:
            print("       ERROR: Scraper not available")