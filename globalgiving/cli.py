import os
import sys
import click
import pymongo
import json
from globalgiving.config import (
    CREDENTIALS_PATH,
    CRED_URI_FIELD,
    CRED_TOKEN_FIELD,
    COMMANDS_HOOK,
    COMMANDS_DIR_NAME,
    COMMANDS_FILE_FULL,
)

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
cmd_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), COMMANDS_DIR_NAME))


class GlobalGiving(click.MultiCommand):
    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(cmd_folder):
            if filename.endswith(".py") and filename.startswith(COMMANDS_HOOK):
                rv.append(filename[4:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            if sys.version_info[0] == 2:
                name = name.encode("ascii", "replace")
            mod = __import__(COMMANDS_FILE_FULL + name, None, None, ["cli"])
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
    with open(os.getenv("HOME") + CREDENTIALS_PATH) as f:
        data = json.load(f)
    try:
        client = pymongo.MongoClient(data[CRED_URI_FIELD])
        db = client.get_database()
        user_information = db["credentials"].find_one(
            {
                CRED_URI_FIELD: data[CRED_URI_FIELD],
                CRED_TOKEN_FIELD: data[CRED_TOKEN_FIELD],
            }
        )
        if user_information is None:
            print("Authentication failed")
            exit(0)
    except:
        print("Authentication failed")
        exit(0)
