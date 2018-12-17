import pytest
from microservices.scraper_hati_malaysia.app import scraper


def test_basic():
    assert scraper.scrape(one=True) is not None
