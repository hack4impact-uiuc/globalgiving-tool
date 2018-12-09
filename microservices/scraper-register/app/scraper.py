from bs4 import BeautifulSoup
import requests
import json


"""Scripts and functions to scrape relevant data from a website."""

# http://org-id.guide/results?structure=all&coverage=all&sector=humantiarian_relief
URL = 'http://org-id.guide/results'
COUNTRY_FILE = 'countries.json'


def scrape():
    """Put everything together and scrape relevant data from the webpage."""
    return "No Data"


def get_registration_site(country):
    """
    Method to get list of registration office website links for a specified country to pair with an NGO.

    param country: specify the country in which to list registration office websites
    """
    payload = {
        'structure': 'all',
        'coverage': country.title(),
        'sector': 'all'
    }
    query_data = requests.get(URL, params=payload)


def get_country_code(country):
    """
    Helper method to find the closest country code for the name passed in.

    param country: specific country to find the country code for
    """
    # Find correct country and country code within lookup JSON
    with open(COUNTRY_FILE, 'r') as f:
        countries = json.loads(f.read())
    
    # Get correct country code by either having a direct match or find the closest match for the given country
    country_code = ''
    if country in countries.keys():
        country_code = countries[country]
    else:
        # Find keys that contain the country parameter within it
        