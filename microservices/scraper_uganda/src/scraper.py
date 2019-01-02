from bs4 import BeautifulSoup
from .models.organization import Org
import requests
import json

website = "https://informationcradle.com/africa/list-of-ngos-in-uganda/"


def scrape_page(ngo):
    name = None
    url = None
    address = None
    phone = None
    email = None
    contact = None
    description = None
    for line in ngo:
        if line[-4:] == "</p>":
            line = line[:-4]
        if line[:3] == "<p>":
            name = line[11:-9]
        elif line[:7] == "P.O.Box":
            _ = line[8:]  # don't have a spot for P.O. box
        elif line[:4] == "www.":
            url = line
        elif line[:8] == "Category":
            _ = line[10:]  # don't currently have category entry spot
        elif line[:16] == "Physical Address":
            address = line[16:]
        elif line[:9] == "Telephone":
            phone = line[11:]
        elif line[:6] == "E-mail":
            email = line[8:]
        elif line[:14] == "Contact Person":
            contact = line[16:]
        else:
            description = line
    return Org(
        name=name,
        url=url,
        address=address,
        phone=phone,
        email=email,
        contact=contact,
        description=description,
        country="Uganda",
    ).to_json()


def get_page_data():
    # Specify url to scrape from
    ret = []
    target_url = requests.get(website)
    page_data = BeautifulSoup(target_url.content, "html.parser")
    contents = page_data.find("div", {"class": "entry-content"})
    contents = contents.find_all("p")
    for ngo in contents:
        ngo = str(ngo).split("<br/>\n")
        ngo_json = scrape_page(ngo)
        ret.append(ngo_json)
    return ret


def get_one():
    # Specify url to scrape from
    ret = []
    target_url = requests.get(website)
    page_data = BeautifulSoup(target_url.content, "html.parser")
    contents = page_data.find("div", {"class": "entry-content"})
    contents = contents.find_all("p")
    # for ngo in contents:
    ngo = str(contents[0]).split("<br/>\n")
    ret.append(scrape_page(ngo))
    return ret[0]
