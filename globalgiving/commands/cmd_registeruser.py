import os, click, jwt, pymongo, dotenv
from globalgiving.cli import pass_context


@click.command("registeruser", short_help="Registers a new user")
@click.option("--key", nargs=1, required=True, type=str)
@pass_context
def cli(ctx, key):
    dotenv.load_dotenv(dotenv.find_dotenv())
    uri = os.getenv("URI")

    client = pymongo.MongoClient(uri)
    db = client.get_database()
    for u in db["whitelist_keys"].find({}):
        print(u)

    whitelist_key = db["whitelist_keys"].find_one({"key": key})

    if whitelist_key is None:
        ctx.log("Whitelist key not found.")
        return

    ctx.log("Enter a username:")
    username = input()
    ctx.log("Enter a password:")
    password = input()

    encoded_jwt = jwt.encode(
        {"mongo_uri": whitelist_key["mongo"]}, "secret", algorithm="HS256"
    )

    try:
        db["users"].insert_one(
            {"user": username, "password": password, "jwt": encoded_jwt}
        )
        ctx.log("Success!")

        with open(".jwt", 'bw+') as f:
            f.write(encoded_jwt)
            f.close()
    except pymongo.errors.DuplicateKeyError:
        ctx.log("Duplicate user name. Please retry with a different username")

    