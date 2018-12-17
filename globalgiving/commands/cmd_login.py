import os
import click
import pymongo
from globalgiving.cli import pass_context
import json


@click.command("register-user", short_help="Login a returning user")
@click.option("--mongo_uri", prompt=True)
@click.option("--token", prompt=True)
@pass_context
def cli(ctx, mongo_uri, token):
    client = pymongo.MongoClient(mongo_uri)

    db = client.get_database()

    user_information = db["credentials"].find_one(
        {"mongo_uri": mongo_uri, "token": token}
    )
    if user_information == None:
        print("You are not authenticated")
        return
    del user_information["_id"]
    if not os.path.exists(os.getenv("HOME") + "/globalgiving/"):
        os.makedirs(os.getenv("HOME") + "/globalgiving/")
    with open(os.getenv("HOME") + "/globalgiving/credentials.json", "w") as f:
        json.dump(user_information, f)
        f.close()
    print("You have succesfully logged in")
