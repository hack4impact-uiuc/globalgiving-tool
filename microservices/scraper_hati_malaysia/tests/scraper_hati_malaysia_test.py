import pytest
from scraper_hati_malaysia.src import scraper


def test_basic():
    assert scraper.scrape(one=True) is not None
