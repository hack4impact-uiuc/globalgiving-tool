import pytest
from scraper_registerids.src.scraper import get_country_code, get_registration_site


def test_current_tags_and_scraping_is_valid():
    # Uses australia to ensure that the current scraping tags, classes, and parsing still produces results
    assert get_registration_site("australia") is not None


def test_country_one_match_case_sensitive():
    assert get_country_code("Afghanistan") == "AF"


def test_country_one_match_case_insensitive():
    assert get_country_code("aFghANisTan") == "AF"


def test_country_one_match_title_case_insensitive():
    assert get_country_code("BoUveT iSlaNd") == "BV"


def test_multiple_countries_first_returned():
    # Assuming python keeps the dictionary keys in order then Democratic People's Republic of Korea should be returned
    assert get_country_code("korea") == "KP"
