import click
from googlesearch import search
from globalgiving.cli import pass_context
from globalgiving.db import db_get_collection
from globalgiving.config import (
    MICROSERVICE_PKG_PATH,
    CRAWL_RANKED_COLLECTION,
)
from urllib.parse import urlparse
import pymongo
import json
import os
import sys


# Bring microservices directory into import path
sys.path.append(os.path.realpath(os.path.dirname(__file__) + MICROSERVICE_PKG_PATH))
from scraper_crawler.crawl_functions import rank_all, url_rank


@click.command("crawl", short_help="Crawl for new directories and NGOs")
@click.argument("country", required=True)
@click.argument("number_urls", required=False)
@pass_context
def cli(ctx, country, number_urls):
    authenticate()
    ranked_link = db_get_collection(CRAWL_RANKED_COLLECTION)
    if not number_urls:
        number_urls = 3
    else:
        number_urls = int(number_urls)

    # Perform google search and start ranking results
    for url in search("ngo directory" + country, lang="es", num=number_urls, stop=1):
        parsed_uri = urlparse(url)
        home_url = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_uri)
        print("Crawling --- ", home_url)
        if str(home_url) not in url_rank:
            #     for url in url_rank:
            # Check if url has already been ranked before
            cursor = ranked_link.find({"url": home_url})
            document_list = [url for url in cursor]
            if len(document_list) == 0:
                url_rank[home_url] = []
                print("Added url " + str(home_url))
            else:
                print("Already have information for " + home_url)
        rank_all(country)

    for url in url_rank:
        print("Inserted " + str(url) + "'s information to database")
        ranked_link.insert_one(url_rank[url])


def dev_crawl(collection, country, number_urls=3):
    """
    Helper method that gets called when testing the command using a mocked collection.

    Input:
        collection: collection to perform operations with/on
        country: country parameter to use for Google search
        number_urls: number of results to rank, defaulted to 3
    """
    for url in search("ngo directory" + country, lang="es", num=number_urls, stop=1):
        parsed_uri = urlparse(url)
        home_url = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_uri)
        if str(home_url) not in url_rank:
            #     for url in url_rank:
            cursor = collection.find({"url": home_url})
            document_list = [url for url in cursor]
            if len(document_list) == 0:
                url_rank[home_url] = []
        rank_all(country)

    for url in url_rank:
        collection.insert_one(url_rank[url])
