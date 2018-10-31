import click
from gg.cli import pass_context
from gg.db import send_to_db


@click.command("register", short_help="Register a new scraper.")
@click.argument("name", required=True)
@click.argument("routes", required=True)
@pass_context
def cli(ctx, name, routes):
    doc_id = send_to_db(name, routes)
    ctx.log("sent to db with id: {}".format(doc_id))
