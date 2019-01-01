import click
import requests
from googlesearch import search
from globalgiving.cli import pass_context
from urllib.parse import urlparse
import dotenv
import os
import sys
import pymongo
from operator import itemgetter
import json

SCRAPER_REG_PATH = "../../../microservices"  # Sibling package path

# Bring microservices directory into import path
sys.path.append(os.path.realpath(os.path.dirname(__file__) + SCRAPER_REG_PATH))
from scraper_crawler.crawl_functions import rank_all, url_rank


@click.command("crawled", short_help="Crawl for new directories and NGOs")
@click.argument("number_urls", required=False)
@pass_context
def cli(ctx, number_urls):

    with open(os.getenv("HOME") + "/globalgiving/credentials.json") as f:
        data = json.load(f)
    uri = data["mongo_uri"]
    client = pymongo.MongoClient(uri)
    db = client.get_database()
    ranked_link = db["ranked_links"]

    cursor = ranked_link.find({})
    directories = [_ for _ in cursor]

    ranked_ngo_directories = []
    for directory in directories:
        ranked_ngo_directories += [(directory["url"], directory["composite_score"])]

    print("Ranked Set of NGO's gathered")
    for ngo_directory in ranked_ngo_directories:
        print("   " + str(ngo_directory[0]) + "  " + str(ngo_directory[1]))
