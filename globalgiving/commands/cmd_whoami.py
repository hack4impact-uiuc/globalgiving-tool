import os
import click
import jwt
from globalgiving.cli import pass_context
from globalgiving.config import CREDENTIALS_PATH, CRED_URI_FIELD, CRED_TOKEN_FIELD
import json


@click.command(
    "whoami", short_help="Get your credentials of the account you are currently in"
)
@pass_context
def cli(ctx):
    if os.path.exists(os.getenv("HOME") + CREDENTIALS_PATH):
        with open(os.getenv("HOME") + CREDENTIALS_PATH) as f:
            data = json.load(f)
        print(
            "You are logged in as "
            + data[CRED_TOKEN_FIELD]
            + " and your mongo uri is "
            + data[CRED_URI_FIELD]
        )
    else:
        print("The file does not exist")
