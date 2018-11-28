import os
import sys
import click, jwt, dotenv, pymongo


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
    Authenticates a user's actions. This is done as follows:
    - grab the user/password pair from the decoded jwt token
    - perform lookup in the table to see if there is a match
    - if yes, then allowed to run any command, otherwise, blocked.
    """

    with open(".jwt", "br+") as f:
        token = f.read()
        decoded = jwt.decode(token, "secret", algorithms="HS256")
        f.close()

    dotenv.load_dotenv(dotenv.find_dotenv())
    uri = os.getenv("URI")

    client = pymongo.MongoClient(uri)
    db = client.get_database()

    users = db["users"].find_one(
        {"user": decoded["user"], "password": decoded["password"]}
    )

    if users is None:
        # presumably, throw some error here.
        # print("error") -> prints are just for debugging at the moment.
        return
    # print("success") -> prints are just for debugging at the moment

