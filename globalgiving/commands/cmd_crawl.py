import click
import requests
from googlesearch import search
from globalgiving.cli import pass_context
from globalgiving.crawler.crawl_functions import rank_all, url_rank
from urllib.parse import urlparse
import dotenv
import pymongo
import json
import os
import sys


@click.command("crawl", short_help="Crawl for new directories and NGOs")
@click.argument("country", required=True)
@click.argument("number_urls", required=False)
@pass_context
def cli(ctx, country, number_urls):
    if not number_urls:
        number_urls = 3
    else:
        number_urls = int(number_urls)

    with open(os.getenv("HOME") + "/globalgiving/credentials.json") as f:
        data = json.load(f)
    client = pymongo.MongoClient(data["mongo_uri"])
    db = client.get_database()
    ranked_link = db["ranked_links"]

    for url in search("ngo directory" + country, lang="es", num=number_urls, stop=1):
        parsed_uri = urlparse(url)
        home_url = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_uri)
        print("Crawling --- ", home_url)
        if str(home_url) not in url_rank:
            #     for url in url_rank:
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
