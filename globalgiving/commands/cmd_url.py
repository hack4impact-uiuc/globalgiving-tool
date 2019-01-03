import click
import requests
from globalgiving.db import db_get_collection, list_scrapers_from_db
from globalgiving.cli import pass_context, authenticate
from globalgiving.config import SCRAPER_COLL_NAME_FIELD
import json


@click.command("url", short_help="Lists all the urls with scrapers")
@click.argument("scraper_name", required=False)
@pass_context
def cli(ctx, scraper_name):
    authenticate()
    collection = db_get_collection()
    scrapers = list_scrapers_from_db(collection)

    # If you have a scraper name, find the url for that scraper
    if scraper_name:
        for scraper in scrapers:
            if scraper[SCRAPER_COLL_NAME_FIELD] == scraper_name:
                url = requests.get(scraper["_id"] + "/url").text
                if "http" in url:
                    print(url)
                    return

    # Otherwise list the names of all sites being scraped
    else:
        for scraper in scrapers:
            print("Scraper: " + scraper[SCRAPER_COLL_NAME_FIELD])
            contents = requests.get(scraper["_id"] + "/url").text
            if "http" in contents:
                print("       " + contents)
            else:
                print("       ERROR: Scraper not available")
