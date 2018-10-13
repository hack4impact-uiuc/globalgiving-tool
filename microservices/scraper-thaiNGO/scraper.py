from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import csv

baseurl = "http://wiki.p2pfoundation.net/NGOs_in_Thailand"

"""
list of dictionaries to store ngo information
ngos = [{
    name: "",
    URL: "",
    phone_num: "",
    email: "",
    registration_id: "",
    year_established: ,
    description: ""
}]
"""
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

"""
DESCRIPTION: scrapes the base directory for links to specific Thai NGO wiki pages        
"""


def basepage_scrape():
    page = requests.get(baseurl)
    soup = BeautifulSoup(page.content, "html5lib")
    # find all NGO entries represented as a row in html table
    ngo_tr_tags = soup.find_all("tr")

    for row in ngo_tr_tags:
        ngo_info = row.find_all("td")
        # dictionary to store ngo information
        ngo = {}
        if ngo_info is not None and len(ngo_info) > 0:
            ngo_name = ngo_info[1]
            ngo["name"] = ngo_name.text.lstrip()
            ngo_descr = ngo_info[2]
            ngo["description"] = ngo_descr.text.lstrip()
            ngo["URL"] = ""
            if ngo_info[3].a is not None:
                ngo_URL = ngo_info[3].a.get("href")
                ngo["URL"] = ngo_URL
            # filter invalid email address formats
            ngo["email"] = ""
            if len(ngo_info[4].text) > 5 and "requested" not in ngo_info[4].text:
                # strip all left spaces, replace @ symbol into email
                ngo_email = ngo_info[4].text.lstrip().replace(" at ", "@")
                ngo["email"] = ngo_email
        # append ngo dictionary to list of ngos
        ngos.append(ngo)

    # write to csv to check output
    keys = ["name", "description", "URL", "email"]
    with open("thai_ngos.csv", "w") as w:
        dict_writer = csv.DictWriter(w, keys)
        dict_writer.writeheader()
        dict_writer.writerows(ngos)

    return ngo_tr_tags
