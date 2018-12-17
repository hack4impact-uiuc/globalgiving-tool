import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join('..', 'microservices', 'scraper_viet')))
from app import scraper


def test_basic():
    assert scraper.get_page_data() is not None
