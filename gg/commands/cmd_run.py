import click, requests
import hashlib
import os
import uuid
from gg.db import list_from_db
from gg.cli import pass_context
from ..s3_interface import *


@click.command("run", short_help="Run a scraper")
@click.option("--n", nargs=1, required=True, type=str)
@pass_context
def cli(ctx, n):
    search = "Finding scraper {} from list of registered scrapers..."
    ctx.log(search.format(n))
    try:
        scrapers = list_from_db()
        route = list(filter(lambda scraper: scraper["name"] == str(n), scrapers))[0][
            "routes"
        ]["Data"]
        ctx.log("Scraper {} found!".format(n))
    except StopIteration:
        ctx.log("Scraper {} not found.".format(n))
        return
    contents = requests.get(route).text
    # ctx.log(contents)

    client = init_s3_credentials()
    h = hashlib.md5()

    h.update(n.encode("utf-8"))
    bucket_name = n + "-" + h.hexdigest()
    
    filename = str(uuid.uuid4()) + '.txt'

    f = open(filename,"w+")
    f.write(contents)
    f.close()

    client.upload_file(filename, bucket_name, filename)
    
    os.remove(filename)
    ctx.log('Wrote logs to file: ' + filename)
