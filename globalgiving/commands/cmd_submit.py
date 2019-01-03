import click
import os
import dotenv
import json
from globalgiving.config import NGO_COLLECTION, CREDENTIALS_PATH, CLI_DIR_NAME
from globalgiving.db import NGO_COLLECTION, db_get_collection, list_ngos_from_db
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
    collection = db_get_collection(NGO_COLLECTION)
    dotenv.load_dotenv(dotenv.find_dotenv())

    # get all NGOs
    ngo_list = list_ngos_from_db(collection)

    # just write to a file for now
    if not os.path.exists(os.getenv("HOME") + CLI_DIR_NAME):
        os.makedirs(os.getenv("HOME") + CLI_DIR_NAME)
    with open(os.getenv("HOME") + CLI_DIR_NAME + "ngo_data.json", "w+") as f:
        f.write(json.dumps(ngo_list, indent=4, separators=(",", ": ")))
    ctx.log("NGO data was successfully submitted!")
