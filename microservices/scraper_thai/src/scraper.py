from bs4 import BeautifulSoup
from .models.organization import Org
import requests
import json
from requests import get
import csv

baseurl = "http://wiki.p2pfoundation.net/NGOs_in_Thailand"

# list of dictionaries to store ngo information
ngos = []
ngos_store_keys = [
    "ngo_name",
    "ngo_URL",
    "phone_num",
    "email",
    "registration_id",
    "year_established",
    "description",
]
ngo_names = {}


def get_test_data():
    page = get(baseurl)
    soup = BeautifulSoup(page.content, "html.parser")
    ngo_tr_tags = soup.find_all("tr")
    ngo_row_scrape(ngo_tr_tags[4])
    return ngos[0]


def get_page_data():
    """
    DESCRIPTION: scrapes the homepage, processes each row for ngo data
    """
    page = get(baseurl)
    soup = BeautifulSoup(page.content, "html.parser")
    # find all NGO entries represented as a row in html table
    ngo_tr_tags = soup.find_all("tr")

    for row in ngo_tr_tags:
        ngo_row_scrape(row)

    return ngos


def ngo_row_scrape(row):
    """
    DESCRIPTION: takes in a table row object, unpacks the data, assembled ngo
                 dictionary to store the data, appends to ngos list
    INPUT: table row object representing information for ngo
    """
    # dictionary to store ngo information
    # ngo = {}
    ngo_info = row.find_all("td")

    # check if row data is valid
    if ngo_info is not None and len(ngo_info) > 0:
        _, ngo_name, ngo_descr, ngo_URL, ngo_email, _ = row.find_all("td")
        name = ngo_name.text.lstrip()
        description = ngo_descr.text.lstrip()
        # check for empty URL
        if ngo_URL.a is not None:
            url = ngo_URL.a.get("href")
        else:
            url = None
        # read email from website if possible
        email = format_ngo_email(ngo_email.text)
        # append ngo dictionary to list of ngos
        org = Org(
            name=name, description=description, url=url, email=email, country="Thailand"
        ).to_json()
        if name not in ngo_names:
            ngos.append(org)
            ngo_names[name] = org


def format_ngo_email(email):
    """
    DESCRIPTION: takes in ngo email read from website and formats it properly,
                 returns empty string if no email can be read
    INPUT: string email read from website
    OUTPUT: properly formatted email string to store
    """
    print(email)
    if "requested" not in email:
        ngo_email = email.lstrip().replace(" at ", "@")
        print(ngo_email)
        return ngo_email
