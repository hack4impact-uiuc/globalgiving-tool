import os
import click
import jwt
import pymongo
from globalgiving.cli import pass_context
from globalgiving.config import (
    CREDENTIALS_PATH,
    CLI_DIR_NAME,
    CRED_URI_FIELD,
    CRED_TOKEN_FIELD,
    CRED_ACCESS_FIELD,
    CRED_SECRET_FIELD,
)
import uuid
import json


@click.command("register", short_help="Registers a new user")
@click.option("--mongo_uri", prompt=True)
@click.option("--access_key", prompt=True)
@click.option("--secret_key", prompt=True)
@pass_context
def cli(ctx, mongo_uri, access_key, secret_key):

    user_information = {
        CRED_URI_FIELD: str(mongo_uri),
        CRED_ACCESS_FIELD: str(access_key),
        CRED_SECRET_FIELD: str(secret_key),
        CRED_TOKEN_FIELD: str(uuid.uuid4()),
    }

    try:
        client = pymongo.MongoClient(mongo_uri)
        db = client.get_database()
        credentials = db["credentials"]
    except:
        print("Invalid mongodb credentials")
        return

    if not os.path.exists(os.getenv("HOME") + CLI_DIR_NAME):
        os.makedirs(os.getenv("HOME") + CLI_DIR_NAME)
    with open(os.getenv("HOME") + CREDENTIALS_PATH, "w") as f:
        json.dump(
            {
                CRED_URI_FIELD: mongo_uri,
                CRED_TOKEN_FIELD: user_information[CRED_TOKEN_FIELD],
            },
            f,
        )
        f.close()

    ctx.log(
        "\nYou have succesfully registered. \nPlease store this token in a safe place "
        + user_information[CRED_TOKEN_FIELD]
    )

    # Adding credentials to the database
    try:
        credentials.insert_one(user_information)
    except pymongo.errors.DuplicateKeyError:
        ctx.log("Duplicate user name. Please retry with a different username")
        return
