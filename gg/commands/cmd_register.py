import click
import requests
from gg.cli import pass_context
from gg.db import send_to_db


@click.command("register", short_help="Register a new scraper.")
@click.argument("name", required=True)
@click.argument("routes", required=True)
@pass_context
def cli(ctx, name, routes):
    """
    Registers the given scraper with the database. It basically just gets all
    possible routes from the `/routes` route then sets up appropriate inputs
    for gg.db.send_to_db().
    """
    try:
        routesList = list(requests.get(routes).json())
    except Exception as ex:
        # source: https://stackoverflow.com/questions/9823936/python-how-do-i-know-what-type-of-exception-occurred
        template = "An exception of type {0} occurred. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        ctx.log(message)
        ctx.log("Getting information from the provided /routes failed.")
        ctx.log("Route tried: {}".format(routes))
        return
    url = routes.replace("/routes", "")
    namesList = [
        name.replace("/", "").replace("<path:filename>", "").title()
        for name in routesList
    ]
    routesList = [url + route.replace("<path:filename>", "") for route in routesList]
    doc_id = send_to_db(name, url, namesList, routesList)
    ctx.log(doc_id)
