import click
import os

from click.testing import CliRunner
from globalgiving.commands.cmd_generate import cli
from globalgiving.commands.cmd_generate import MS_DIR


PYCACHE = "__pycache__"
DELIM = "_"
SCRAPER_DELIM = "scraper"


def get_first_scraper():
    """Helper method to get the first existing scraper in microservices for testing."""
    # Get root directory and set start of existing scraper search to the root microservices directory
    rootdir = os.pardir + MS_DIR
    subdir_list = next(os.walk(rootdir))[1]

    # Get first non pycache scraper
    for directory in subdir_list:
        if directory != PYCACHE:
            # Split directory to get the name without extra scraper_
            # ASSUMES that microservices start with tag (scraper, etc.) followed by underscore
            dir_split = directory.split(DELIM, 1)
            return dir_split[1]


def get_num_scrapers():
    """Helper method to get the number of scrapers"""
    # Get root directory and set start of existing scraper search to the root microservices directory
    rootdir = os.pardir + MS_DIR
    subdir_list = next(os.walk(rootdir))[1]

    # Return the number of scrapers
    scraper_list = list(filter(lambda x:SCRAPER_DELIM in x, subdir_list))
    return len(scraper_list)


def test_generate_existing():
    # Get first existing scraper for testing an existing microservice
    existing_name = get_first_scraper()
    prev_num_scrapers = get_num_scrapers()

    # Setup click testing and command invocation
    runner = CliRunner()
    result = runner.invoke(cli, [existing_name])

    # Check that the number of scrapers hasn't changed (successfully found existing scraper)
    assert prev_num_scrapers == get_num_scrapers()

