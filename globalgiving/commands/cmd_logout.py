import os
import click
import jwt
from globalgiving.cli import pass_context

@click.command("logout", short_help="Registers a new user")
@pass_context
def cli(ctx):
    if os.path.exists(".jwt"):
        os.remove(".jwt")
        print("You are logged out")
    else:
        print("The file does not exist")
    