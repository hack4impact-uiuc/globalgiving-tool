import os
import click
import jwt
from globalgiving.cli import pass_context
import json


@click.command(
    "whoami", short_help="Get your credentials of the account you are currently in"
)
@pass_context
def cli(ctx):
    if os.path.exists(os.getenv("HOME") + "/globalgiving/" + "credentials.json"):
        with open(os.getenv("HOME") + "/globalgiving/credentials.json") as f:
            data = json.load(f)
        print(
            "You are logged in as "
            + data["token"]
            + " and your mongo uri is "
            + data["mongo_uri"]
        )
    else:
        print("The file does not exist")
