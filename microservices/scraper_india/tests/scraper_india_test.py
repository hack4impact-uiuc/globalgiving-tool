import pytest
from scraper_india.src import scraper


def test_basic():
    assert scraper.get_one_nonprofit() is not None
