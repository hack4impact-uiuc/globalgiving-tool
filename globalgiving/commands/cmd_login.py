import os
import click
import jwt
import pymongo
import dotenv
from globalgiving.cli import pass_context

@click.command("register-user", short_help="Registers a new user")
@click.option('--username', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
@pass_context
def cli(ctx, username, password):
    # endpoint containing db of users and whitelist keys
    dotenv.load_dotenv(dotenv.find_dotenv())
    uri = os.getenv("URI")

    client = pymongo.MongoClient(uri)
    db = client.get_database()

    user = (db["users"].find_one({"user": username, "password": password}))
    if (user is None):
        print("Incorrect username or password, please try logging in again")
    else:
        with open(".jwt", "wb") as f:
            f.write(user["jwt"])
            f.close()
        ctx.log(username + " is successfully logged in!")