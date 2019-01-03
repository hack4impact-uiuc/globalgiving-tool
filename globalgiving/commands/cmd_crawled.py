import click
from globalgiving.cli import pass_context
from globalgiving.db import db_get_collection
import pymongo
from globalgiving.config import MICROSERVICE_PKG_PATH, CRAWL_RANKED_COLLECTION
from urllib.parse import urlparse
import os
import sys
import json


# Bring microservices directory into import path
sys.path.append(os.path.realpath(os.path.dirname(__file__) + MICROSERVICE_PKG_PATH))
from scraper_crawler.crawl_functions import rank_all, url_rank


@click.command("crawled", short_help="Crawl for new directories and NGOs")
@pass_context
def cli(ctx):
    authenticate()
    ranked_link = db_get_collection(CRAWL_RANKED_COLLECTION)
    cursor = ranked_link.find({})
    directories = [_ for _ in cursor]

    ranked_ngo_directories = []
    for directory in directories:
        ranked_ngo_directories += [(directory["url"], directory)]

    print("Ranked Set of NGO's gathered")
    for ngo_directory in ranked_ngo_directories:
        print("   " + str(ngo_directory[0]))
        rank_info = ngo_directory[1]
        print("         Has " + str(rank_info["num_phone_numbers"]) + " phone numbers")
        print("         Has " + str(rank_info["num_addresses"]) + " addresses")
        print("         Has " + str(rank_info["num_subpages"]) + " subpages")
        print(
            "         Has "
            + str(rank_info["num_word_ngo"])
            + " appearances of ngo directory related words"
        )


def dev_crawled(collection):
    """
    Helper method that gets called when testing the command using a mocked collection.

    Input:
        collection: collection to perform operations with/on
    """
    cursor = collection.find({})
    directories = [_ for _ in cursor]

    ranked_ngo_directories = []
    for directory in directories:
        ranked_ngo_directories += [(directory["url"], directory["composite_score"])]

    return ranked_ngo_directories
