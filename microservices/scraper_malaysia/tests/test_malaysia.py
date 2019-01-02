import pytest
from scraper_malaysia.src.scraper import (
    scrape,
    get_cat_links,
    get_ngo_links,
    get_ngo_information,
)


def test_basic():
    assert scrape(one=True) is not None


def test_sections():
    # get the categories
    categories = get_cat_links()
    number_of_categories = 39  # from hati.my
    # if this test fails, then either the scraper has failed or the source
    # website has changed.
    assert len(categories) == number_of_categories

    # get the links associated with a couple categories
    links = get_ngo_links(categories[:2])
    # we will use an approximate number for this test as the categories can
    # sometimes appear in different orders
    minimum_links = 3
    assert len(links) > minimum_links

    # check if the links are valid by getting a couple sets of information
    information = get_ngo_information(links[:2])
    for ngo in information:
        assert ngo is not None
