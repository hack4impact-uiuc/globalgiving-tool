import pytest
from microservices.example_scraper import scraper


def test_basic():
    assert scraper.get_page_data() is not None
