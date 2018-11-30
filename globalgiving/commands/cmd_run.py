import click, requests

import hashlib
import os
import uuid
from globalgiving.db import list_from_db
from globalgiving.cli import pass_context, authenticate
from ..s3_interface import *


@click.command("run", short_help="Run a scraper")
@click.argument("n", required=True)
@pass_context
def cli(ctx, n):
    authenticate()
    client = init_s3_credentials()

    h = hashlib.md5()
    h.update(n.encode("utf-8"))
    bucket_name = n + "-" + h.hexdigest()

    filename = str(uuid.uuid4()) + ".txt"
    f = open(filename, "w+")

    search = "Finding scraper {} from list of registered scrapers..."
    f.write(search.format(n) + "\n")
    try:
        scrapers = list_from_db()
        route = list(filter(lambda scraper: scraper["name"] == str(n), scrapers))[0][
            "routes"
        ]["Data"]
        f.write("Scraper {} found!".format(n) + "\n")
    except StopIteration:
        f.write("Scraper {} not found!".format(n) + "\n")
        f.close()
        client.upload_file(filename, bucket_name, filename)
        os.remove(filename)
        return
    try:
        contents = requests.get(route).text + "\nSUCCESS"
    except Exception as e:
        contents = str(e) + "\nFAILED"

    f.write(contents)
    f.close()

    # Call S3 to list current buckets
    response = client.list_buckets()

    # Get a list of all bucket names from the response
    buckets = [bucket["Name"] for bucket in response["Buckets"]]

    if not (bucket_name in buckets):
        client.create_bucket(Bucket=bucket_name)

    client.upload_file(filename, bucket_name, filename)

    os.remove(filename)
    ctx.log("Wrote logs to file: " + filename)
