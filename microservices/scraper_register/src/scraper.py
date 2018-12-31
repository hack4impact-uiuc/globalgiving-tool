from bs4 import BeautifulSoup
from models.countries import countries
import requests
import json


"""Scripts and functions to scrape relevant data from a website."""

# http://org-id.guide/results?structure=all&coverage=all&sector=humantiarian_relief
URL = "http://org-id.guide/results"
COUNTRY_PATH = "models/countries.json"


def scrape():
    """Put everything together and scrape relevant data from the webpage."""
    return "No Data"


def get_registration_site(country):
    """
    Method to get list of registration office website links for a specified country to pair with an NGO.

    param country: specify the country in which to list registration office websites
    """
    # Specify search query string parameters
    payload = {
        "structure": "all",
        "coverage": get_country_code(country.title()),
        "sector": "all",
    }

    # Inject search into website and get list of registration sites
    query_data = requests.get(URL, params=payload)
    soup = BeautifulSoup(query_data.content, "html.parser")
    found_sites = soup.find_all("footer", class_="card__controls")

    # Loop through resulting links and return the first office site, which is the most relevant
    # Each footer has nested elements, the first of which is a newline escaped character
    # The second is the link that we want that has the site of the registration office
    url = found_sites[0].contents[1]["href"]
    return url


def get_country_code(country):
    """
    Helper method to find the closest country code for the name passed in.

    param country: specific country to find the country code for
    """

    # Get correct country code by either having a direct match or find the closest match for the given country
    country_code = ""
    if country in countries.keys():
        country_code = countries[country]
    else:
        # Find keys that contain the country parameter within it and select the first one
        for code in countries.keys():
            if country in code:
                country_code = code
                break

    return country_code
