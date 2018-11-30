import os
import click
import jwt
import pymongo
import dotenv
from globalgiving.cli import pass_context


@click.command("register-user", short_help="Registers a new user")
@click.option("--key", prompt=True)
@click.option("--username", prompt=True)
@click.option("--password", prompt=True, hide_input=True, confirmation_prompt=True)
@pass_context
def cli(ctx, key, username, password):
    # endpoint containing db of users and whitelist keys
    dotenv.load_dotenv(dotenv.find_dotenv())
    uri = os.getenv("URI")
    client = pymongo.MongoClient(uri)
    db = client.get_database()

    whitelist_key = db["whitelist_keys"].find_one({"key": key})
    if whitelist_key is None:
        ctx.log("Whitelist key not found.")
        return

    encoded_jwt = jwt.encode(
        {"user": username, "password": password, "mongo_uri": whitelist_key["mongo"]},
        "secret",
        algorithm="HS256",
    )

    try:
        db["users"].insert_one(
            {"user": username, "password": password, "jwt": encoded_jwt}
        )
        ctx.log("Success!")
    except pymongo.errors.DuplicateKeyError:
        ctx.log("Duplicate user name. Please retry with a different username")
        return

    # write jw token to a file - this is used for authentication of other commands
    with open(".jwt", "wb") as f:
        f.write(encoded_jwt)
        f.close()
