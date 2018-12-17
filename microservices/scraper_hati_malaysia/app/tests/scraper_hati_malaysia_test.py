import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join("..", "microservices")))

from scraper_hati_malaysia.app import scraper


def test_basic():
    assert scraper.scrape(one=True) is not None
