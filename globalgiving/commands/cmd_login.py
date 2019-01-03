import os
import click
import pymongo
from globalgiving.cli import pass_context
from globalgiving.db import db_get_collection
from globalgiving.config import (
    CREDENTIALS_PATH,
    CRED_URI_FIELD,
    CLI_DIR_NAME,
    CRED_TOKEN_FIELD,
    CRED_COLLECTION,
)
import json


@click.command("register-user", short_help="Login a returning user")
@click.option("--mongo_uri", prompt=True)
@click.option("--token", prompt=True)
@pass_context
def cli(ctx, mongo_uri, token):
    collection = db_get_collection(CRED_COLLECTION)
    user_information = collection.find_one(
        {CRED_URI_FIELD: mongo_uri, CRED_TOKEN_FIELD: token}
    )
    if user_information == None:
        print("You are not authenticated")
        return
    del user_information["_id"]
    if not os.path.exists(os.getenv("HOME") + CLI_DIR_NAME):
        os.makedirs(os.getenv("HOME") + CLI_DIR_NAME)
    with open(os.getenv("HOME") + CREDENTIALS_PATH, "w") as f:
        json.dump({CRED_URI_FIELD: mongo_uri, CRED_TOKEN_FIELD: token}, f)
        f.close()
    print("You have succesfully logged in")
