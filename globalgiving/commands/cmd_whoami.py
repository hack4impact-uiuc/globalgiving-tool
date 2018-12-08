import os
import click
import jwt
from globalgiving.cli import pass_context


@click.command("whoami", short_help="Registers a new user")
@pass_context
def cli(ctx):
    try:
        with open(os.getenv("HOME") + "/globalgiving/" + ".jwt", "rb") as f:
            byte = f.read()
            decoded = jwt.decode(byte, "secret", algorithms=["HS256"])
            print("You are logged in as " + decoded["user"])
    except:
        print("You are not currently logged in")
