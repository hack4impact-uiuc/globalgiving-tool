import pytest
from scraper_viet.app import scraper

def test_basic():
    assert scraper.get_page_data() is not None