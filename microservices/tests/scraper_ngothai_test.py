import pytest
from microservices.scraper_ngothai.app import scraper


def test_basic():
    assert scraper.get_one_ngo() is not None
