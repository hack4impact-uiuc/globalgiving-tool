import click
import requests
from googlesearch import search
from globalgiving.cli import pass_context
from globalgiving.crawler.crawl_functions import rank_all, url_rank
from urllib.parse import urlparse
import dotenv
import os
import pymongo
from operator import itemgetter


@click.command("crawled", short_help="Crawl for new directories and NGOs")
@click.argument("number_urls", required=False)
@pass_context
def cli(ctx, number_urls):

    dotenv.load_dotenv(dotenv.find_dotenv())
    uri = os.getenv("URI")
    client = pymongo.MongoClient(uri)
    db = client.get_database()
    ranked_link = db["ranked_links"]

    cursor = ranked_link.find({})
    directories = [_ for _ in cursor]

    ranked_ngo_directories = []
    for directory in directories:
        ranked_ngo_directories += [(directory["url"], directory["composite_score"])]

    ranked_ngo_directories = sorted(ranked_ngo_directories, key=itemgetter(1))[::-1]
    print("Ranked Set of NGO's gathered")
    for ngo_directory in ranked_ngo_directories:
        print("   " + ngo_directory[0] + "  " + ngo_directory[1])
