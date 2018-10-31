import click
import requests
from gg.cli import pass_context
from gg.db import send_to_db


@click.command("register", short_help="Register a new scraper.")
@click.argument("name", required=True)
@click.argument("routes", required=True)
@pass_context
def cli(ctx, name, routes):
    try:
        routesList = list(requests.get(routes).json())
    except Exception as e:
        ctx.log(e)
        ctx.log("Getting information from the provided /routes failed.")
        ctx.log("Route tried: {}".format(routes))
        return
    url = routes.replace("/routes", "")
    namesList = [
        name.replace("/", "").replace("<path:filename>", "").title()
        for name in routesList
    ]
    routesList = [url + route.replace("<path:filename>", "") for route in routesList]
    ctx.log(routesList)
    ctx.log(namesList)
    doc_id = send_to_db(name, url, namesList, routesList)
    ctx.log("sent to db with id: {}".format(doc_id))
