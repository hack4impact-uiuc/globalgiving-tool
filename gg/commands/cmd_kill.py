import click, jwt, pymongo
from gg.cli import pass_context


@click.command("kill", short_help="kill a currently running scraper")
@click.option("--n", nargs=1, required=True, type=str)
@pass_context
def cli(ctx, n):
    print(n)
