import pytest
from microservices.scraper_ngouganda.app import scraper


def test_basic():
    assert scraper.get_one() is not None
