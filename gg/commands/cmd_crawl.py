import click
import requests
from gg.cli import pass_context
from googlesearch import search

@click.command("crawl", short_help="Crawl for new directories and NGOs")
@click.argument("country", required=True)
@click.argument("ngo_type", required=True)
@pass_context

def cli(ctx,country,ngo_type):
    for url in search('ngo directory' + country + ngo_type, lang='es', num=10, pause=2.0, stop=20):
        print(url)
