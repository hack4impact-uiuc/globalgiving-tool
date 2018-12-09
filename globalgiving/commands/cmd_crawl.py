import click
import requests
from googlesearch import search
from globalgiving.cli import pass_context
from globalgiving.crawler.crawl_functions import rank_all, url_rank
from urllib.parse import urlparse


@click.command("crawl", short_help="Crawl for new directories and NGOs")
@click.argument("country", required=True)
@pass_context
def cli(ctx, country):
    urls = []
    for url in search("ngo directory" + country, lang="es", num=5, stop=1):
        parsed_uri = urlparse(url)
        home_url = "{uri.scheme}://{uri.netloc}/".format(uri=parsed_uri)
        if str(home_url) not in url_rank:
            print("Added url " + str(home_url))
            url_rank[home_url] = []
    rank_all(country)

    print(url_rank)
