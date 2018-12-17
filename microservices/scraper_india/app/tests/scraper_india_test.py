import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join("..", "microservices")))

from scraper_india.app import scraper


def test_basic():
    assert scraper.get_one_nonprofit() is not None
