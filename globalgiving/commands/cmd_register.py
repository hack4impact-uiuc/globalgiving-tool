import os
import click
import jwt
import pymongo
from globalgiving.cli import pass_context
import uuid
import json


@click.command("register", short_help="Registers a new user")
@click.option("--mongo_uri", prompt=True)
@click.option("--access_key", prompt=True)
@click.option("--secret_key", prompt=True)
@pass_context
def cli(ctx, mongo_uri, access_key, secret_key):

    user_information = {
        "mongo_uri": str(mongo_uri),
        "access_key": str(access_key),
        "secret_key": str(secret_key),
        "token": str(uuid.uuid4()),
    }

    try:
        client = pymongo.MongoClient(mongo_uri)
        db = client.get_database()
        credentials = db["credentials"]
    except:
        print("Invalid mongodb credentials")
        return

    if not os.path.exists(os.getenv("HOME") + "/globalgiving/"):
        os.makedirs(os.getenv("HOME") + "/globalgiving/")
    with open(os.getenv("HOME") + "/globalgiving/credentials.json", "w") as f:
        json.dump(user_information, f)
        f.close()

    ctx.log(
        "\nYou have succesfully registered. \nPlease store this token in a safe place "
        + user_information["token"]
    )

    # Adding credentials to the database
    try:
        credentials.insert_one(user_information)
    except pymongo.errors.DuplicateKeyError:
        ctx.log("Duplicate user name. Please retry with a different username")
        return
