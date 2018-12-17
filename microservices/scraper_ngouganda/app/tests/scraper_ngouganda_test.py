import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join("..", "microservices")))
from scraper_ngouganda.app import scraper


def test_basic():
    assert scraper.get_one() is not None
