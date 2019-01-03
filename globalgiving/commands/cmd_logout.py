import os
import click
from globalgiving.cli import pass_context
from globalgiving.config import CREDENTIALS_PATH


@click.command("logout", short_help="Logout the current active user")
@pass_context
def cli(ctx):
    if os.path.exists(os.getenv("HOME") + CREDENTIALS_PATH):
        os.remove(os.getenv("HOME") + CREDENTIALS_PATH)
        print("You are logged out")
    else:
        print("The file does not exist")
