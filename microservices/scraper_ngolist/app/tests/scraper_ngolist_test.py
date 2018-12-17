import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join("..", "microservices")))
from scraper_ngolist.app import scraper


def test_basic():
    assert scraper.basepage_scrape() is not None
