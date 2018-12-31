import click
import requests
from globalgiving.db import list_scrapers_from_db
from globalgiving.cli import pass_context, authenticate
import json


@click.command("url", short_help="Lists all the urls with scrapers")
@click.option(
    "--scraper_name",
    help="the name of the scraper which we are getting the url for",
    required=False,
    default=None,
)
@pass_context
def cli(ctx, scraper_name):
    authenticate()
    scrapers = list_scrapers_from_db()
    if scraper_name:
        for scraper in scrapers:
            if scraper["name"] == scraper_name:
                url = requests.get("http://" + scraper["_id"] + "/url").text
                if "http" in url:
                    print(url)
                    return

    for scraper in scrapers:
        print("Scraper: " + scraper["name"])
        # contents = requests.get(scraper["routes"]["Test"][0:-4] + "url").text
        contents = requests.get("http://" + scraper["_id"] + "/url").text
        if "http" in contents:
            print("       " + contents)
        else:
            print("       ERROR: Scraper not available")
