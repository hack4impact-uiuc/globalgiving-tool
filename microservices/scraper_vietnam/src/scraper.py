from bs4 import BeautifulSoup
from requests import get
import json
from .models.organization import Org

url = "https://www.viet.net/community/nonprofit/"


def create_org(line):

    """
    Attempts to parse a line of data into the Org class.
     Input:
        line: an array of strings that could possibly contain organization data.
        Lines are usually arranged as such [ 'name' , 'key:value' ], where key 
        would be a specific field (one of name, phone, email, etc.) and value 
        would be that specific piece of data for the field.
         Some lines do not correspond to this format and do not contain useful
        information.
     Returns:
        If the line contains valid organization data, then we return a serialized 
        Org object containing the data in the input line. Otherwise, we'll return 
        None.
    """
    valid_categories = ["name", "phone", "email", "address", "contact", "url"]
    org_data = {}

    for idx, info in enumerate(line):
        if idx == 0:
            name = info
            continue
        if ":" not in info:
            continue

        delim = info.split(":", 1)
        category = delim[0].lower()
        data = delim[1].strip()

        if category in valid_categories:
            org_data[category] = data

    phone = org_data["phone"] if "phone" in org_data.keys() else None
    email = org_data["email"] if "email" in org_data.keys() else None
    address = org_data["address"] if "address" in org_data.keys() else None
    contact = org_data["contact"] if "contact" in org_data.keys() else None
    url = org_data["url"] if "url" in org_data.keys() else None

    if bool(org_data):
        org = Org(
            name=name,
            phone=phone,
            email=email,
            address=address,
            contact=contact,
            url=url,
            country="Vietnam",
        ).to_json()
        # print(line)
        return org
    return None


def parse_data(link):
    orgs = []
    if link != None:
        for line in link.split("\n\n"):
            org = create_org(line.strip().split("\n"))
            if org is not None:
                orgs += [org]
    return orgs


def get_page_data():
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    orgs = {}
    for link in soup.findAll("p")[:]:
        new_orgs = parse_data(link.text)
        for org in new_orgs:
            orgs[org["name"]] = org
    return list(orgs.values())


def get_test_data():
    response = get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    return parse_data((soup.findAll("p")[0]).text)[0]
