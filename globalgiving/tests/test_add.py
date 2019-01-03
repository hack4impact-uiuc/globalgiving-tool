import click
import mongomock
import os

from click.testing import CliRunner
from globalgiving.commands.cmd_add import dev_add


def test_add_one():
    # mock collection for testing
    mock_collection = mongomock.MongoClient().db.collection

    # set up mocked scraper to submit
    name = "test"
    url = "https://gg-scraper-example.now.sh"

    # call `dev_add` which mirror what the cli version does
    result = dev_add(mock_collection, name, url)

    # test for expected result
    assert result == url

    # submit again
    result = dev_add(mock_collection, name, url)

    # make sure it updates
    assert result == "Updated scraper {}!\n".format(name) + url
