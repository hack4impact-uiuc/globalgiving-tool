import click
from complex.cli import pass_context


@click.command("whereami", short_help="Gives you your current directory")
@click.argument("path", required=False, type=click.Path(resolve_path=True))
@pass_context
def cli(ctx, path):
    if path is None:
        path = ctx.home
    ctx.log("My current directory is %s", click.format_filename(path))
