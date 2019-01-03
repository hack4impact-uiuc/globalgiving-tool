import click
import hashlib
from ..s3_interface import *
from tabulate import tabulate
from globalgiving.cli import pass_context, authenticate


@click.command(
    "log", short_help="Gives all runs for the scraper with associated s3-names"
)
@click.argument("scraper_name", required=False)
@click.argument("filename", required=False)
@pass_context
def cli(ctx, scraper_name, filename):
    authenticate()
    client = init_s3_credentials()

    # Generate bucket name to fetch logs from
    h = hashlib.md5()
    h.update(scraper_name.encode("utf-8"))
    bucket_name = scraper_name + "-" + h.hexdigest()

    # Attempt to find bucket for logs
    if not filename:
        response = client.list_buckets()
        if bucket_name not in [bucket["Name"] for bucket in response["Buckets"]]:
            ctx.log("The provided scraper has no logs!")
            return
        else:
            objects = client.list_objects(Bucket=bucket_name)["Contents"]
            parsed = [[i["Key"], i["LastModified"]] for i in objects]
            table = tabulate(parsed, headers=["File Name", "Last Modified"])
            print(table)
            return
    else:
        client.download_file(Bucket=bucket_name, Key=filename, Filename=filename)
        ctx.log("Downloaded file to: %s", click.format_filename(filename))
        return
