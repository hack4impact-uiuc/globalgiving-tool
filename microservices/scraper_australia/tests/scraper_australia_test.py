import pytest
import sys, os
from scraper_australia.src import scraper

# sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))

def test_basic():
    #print(os.path.realpath(os.path.dirname(__file__)+"/.."))
    assert scraper.get_page_data() is not None
