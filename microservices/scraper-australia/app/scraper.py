from bs4 import BeautifulSoup
from microservices.models.organization import Org
import requests
import json

website = "http://www.findouter.com/Oceania/Australia/Society-and-Culture/Non-Governmental-Organisations/"


def get_one_nonprofit():
    return parse_page(website + "1")[0]


def parse_page(webpage):
    list_of_ds = []
    target_url = requests.get(webpage)
    page_data = BeautifulSoup(target_url.content, "html.parser")
    contents = page_data.find("div", {"class": "container"})
    for ngo in str(contents).split('<div class="firstline">\n')[1:]:
        # print(ngo)
        website = None
        name = None
        telephone = None
        address = None
        description = None
        for line in ngo.split("\n"):
            if line[:23] == '<span class="sitename">':
                line = line.split(">")
                website = line[1].split('"')[1]
                name = line[2][:-3]
            elif line[:20] == '<span class="phone">':
                telephone = line[25:40]
            elif line[:22] == '<span class="address">':
                line = line.split(">")
                address = line[1][:-6]
            elif line[:25] == '<div class="description">':
                line = line.split(">")
                description = line[1][:-5]
        list_of_ds.append(
            Org(
                name=name,
                phone=telephone,
                address=address,
                description=description,
                url=website,
                country="Australia",
            ).to_json()
        )
    return list_of_ds


def get_page_data():
    ret = []
    for i in range(1, 7):
        webpage = website + str(i)
        ret.extend(parse_page(webpage))
    return json.dumps(ret)
