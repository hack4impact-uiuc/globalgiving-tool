import pytest
from scraper_india.app import scraper

def test_basic():
    assert scraper.get_one_nonprofit() is not None