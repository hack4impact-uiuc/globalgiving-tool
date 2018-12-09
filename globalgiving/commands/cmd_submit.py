import click
import os
import dotenv
import json
from globalgiving.db import list_ngos_from_db
from globalgiving.cli import pass_context, authenticate


@click.command("submit", short_help="Submit NGO data to API")
@pass_context
def cli(ctx):
    """
    Submits all NGO data stored in the MLab database to the GlobalGiving API.
    TEMPORARY STUB: Currently, the data is just stored in
    `~/globalgiving/ngo_data.json`
    """
    authenticate()
    dotenv.load_dotenv(dotenv.find_dotenv())

    # get all NGOs
    ngo_list = list_ngos_from_db()

    # just write to a file for now
    if not os.path.exists(os.getenv("HOME") + "/globalgiving/"):
        os.makedirs(os.getenv("HOME") + "/globalgiving/")
    with open(os.getenv("HOME") + "/globalgiving/" + "ngo_data.json", "w+") as f:
        f.write(json.dumps(ngo_list, indent=4, separators=(",", ": ")))
    ctx.log("NGO data was successfully submitted!")
