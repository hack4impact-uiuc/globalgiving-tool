from bs4 import BeautifulSoup
from .models.countries import countries
import requests
import json


"""Scripts and functions to scrape relevant data from a website."""


URL = "http://org-id.guide/results"
COUNTRY_PATH = "models/countries.json"

PARSER = "html.parser"
SITE_TAG = "footer"
TAG_CLASS = "card__controls"
TAG_ATTR = "href"


def scrape():
    """Put everything together and scrape relevant data from the webpage."""
    return "No Data"


def get_registration_site(country):
    """
    Method to get list of registration office website links for a specified country to pair with an NGO.
    Website for reference: http://org-id.guide/results?structure=all&coverage=all&sector=humantiarian_relief

    param country: specify the country in which to list registration office websites
    """
    # Specify search query string parameters
    payload = {
        "structure": "all",
        "coverage": get_country_code(country),
        "sector": "all",
    }

    # Inject search into website and get list of registration sites
    query_data = requests.get(URL, params=payload)
    soup = BeautifulSoup(query_data.content, PARSER)
    found_sites = soup.find_all(SITE_TAG, class_=TAG_CLASS)

    # Loop through resulting links and return the first office site, which is the most relevant
    # Each footer has nested elements, the first of which is a newline escaped character
    # The second is the link that we want that has the site of the registration office
    url = found_sites[0].contents[1][TAG_ATTR]
    return url


def get_country_code(country):
    """
    Helper method to find the closest country code for the name passed in.

    param country: specific country to find the country code for
    """
    # Convert to title case to match countries json
    country = country.title()

    # Get correct country code by either having a direct match or find the closest match for the given country
    country_code = ""
    if country in countries.keys():
        country_code = countries[country]
    else:
        # Find keys that contain the country parameter within it and select the first one
        for name in countries.keys():
            if country in name:
                country_code = countries[name]
                break

    return country_code
