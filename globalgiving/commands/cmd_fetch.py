import os, click, jwt, pymongo, dotenv
from globalgiving.config import CLI_DIR_NAME
from globalgiving.cli import pass_context


@click.command("fetch", short_help="Fetch jw token for a registered user")
@click.option("--user", nargs=1, required=True, type=str)
@click.option("--password", nargs=1, required=True, type=str)
@pass_context
def cli(ctx, user, password):
    # endpoint containing db of users and whitelist keys
    dotenv.load_dotenv(dotenv.find_dotenv())
    uri = os.getenv("URI")

    client = pymongo.MongoClient(uri)
    db = client.get_database()

    jwtoken = db["users"].find_one({"user": user, "password": password})["jwt"]

    if jwtoken is None:
        ctx.log("authentication failed - no jw token found for given user information")
        return

    # write jw token to a file
    with open(os.getenv("HOME") + CLI_DIR_NAME + ".jwt", "wb") as f:
        f.write(jwtoken)
        f.close()

    ctx.log("successfully fetched jw token, saved locally as .jwt")
