import os
import click
import jwt
from globalgiving.cli import pass_context


@click.command("logout", short_help="Logout the current active user")
@pass_context
def cli(ctx):
    if os.path.exists(os.getenv("HOME") + "/globalgiving/" + "credentials.json"):
        os.remove(os.getenv("HOME") + "/globalgiving/" + "credentials.json")
        print("You are logged out")
    else:
        print("The file does not exist")
