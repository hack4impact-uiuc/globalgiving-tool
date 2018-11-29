import os
import sys
import click
import jwt
import dotenv
import pymongo

CONTEXT_SETTINGS = dict(auto_envvar_prefix="GlobalGiving")


class Context(object):
    def __init__(self):
        self.verbose = False
        self.home = os.getcwd()

    def log(self, msg, *args):
        """Logs a message to stderr."""
        if args:
            msg %= args
        click.echo(msg, file=sys.stderr)

    def vlog(self, msg, *args):
        """Logs a message to stderr only if verbose is enabled."""
        if self.verbose:
            self.log(msg, *args)


pass_context = click.make_pass_decorator(Context, ensure=True)
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "commands"))


class GlobalGiving(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith("cmd_"):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode("ascii", "replace")
            mod = __import__("globalgiving.commands.cmd_" + name, None, None, ["cli"])
        except ImportError:
            return
        return mod.cli


@click.command(cls=GlobalGiving, context_settings=CONTEXT_SETTINGS)
@pass_context
def cli(ctx, verbose=False):
    """A complex command line interface."""
    ctx.verbose = verbose


def authenticate():
    """
    Authenticates a request to run any command (other than registeruser).
    This is done by using the jw token stored locally and performing a lookup
    of user/password pairs with the database.
    """
    dotenv.load_dotenv(dotenv.find_dotenv())
    uri = os.getenv("URI")

    client = pymongo.MongoClient(uri)
    db = client.get_database()

    try:
        with open(".jwt", "rb") as jwt_file:
            encoded_jwt = jwt_file.read()
    except FileNotFoundError:
        print("No JW token found")
        exit(0)

    auth_info = jwt.decode(encoded_jwt, "secret", algorithms=["HS256"])
    user_match = db["users"].find_one(
        {"user": auth_info["user"], "password": auth_info["password"]}
    )

    if user_match is None:
        print("Authentication failed")
        exit(0)
