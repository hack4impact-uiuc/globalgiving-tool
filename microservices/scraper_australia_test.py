import pytest
from microservices.scraper_australia.app import scraper


def test_basic():
    assert scraper.get_page_data() is not None