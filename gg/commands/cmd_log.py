import click
from ..s3_interface import *
from tabulate import tabulate
from gg.cli import pass_context


@click.command(
    "log", short_help="Gives all runs for the scraper with associated s3-names"
)
@click.option(
    "--bucket_name",
    help="The name of the scraper that logs will be outputted from",
    required=True,
    default=None,
)
@click.option(
    "--filename",
    help="The s3 name of the log that will be outputted",
    required=False,
    default=None,
)
@pass_context
def cli(ctx, bucket_name, filename):
    # if (not bucket_name and not filename) or (bucket_name and filename):
    #     ctx.log("Please specify either bucket_name or filename!")
    #     return
    client = init_s3_credentials()
    # client.create_bucket(Bucket='test-bucket-jingtao-1')
    # filename = 'requirements.txt'
    # client.upload_file(filename, bucket_name, filename)
    if not filename:  # MAKE IT SO THE SCRAPER NAME MAPS TO S3 BUCKET NAME
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
        ctx.log("Downladed file to: %s", click.format_filename(filename))
        return
