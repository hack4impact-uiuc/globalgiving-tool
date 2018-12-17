import pytest
from microservices.scraper_ngolist.app import scraper


def test_basic():
    assert scraper.basepage_scrape() is not None
