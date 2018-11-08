from bs4 import BeautifulSoup
import requests
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


def get_one_ngo():
    page = get(baseurl)
    soup = BeautifulSoup(page.content, "html.parser")
    ngo_tr_tags = soup.find_all("tr")
    ngo_row_scrape(ngo_tr_tags[4])
    return ngos[0]


def basepage_scrape():
    """
    DESCRIPTION: scrapes the homepage, processes each row for ngo data
    """
    page = get(baseurl)
    soup = BeautifulSoup(page.content, "html.parser")
    # find all NGO entries represented as a row in html table
    ngo_tr_tags = soup.find_all("tr")

    for row in ngo_tr_tags:
        ngo_row_scrape(row)

    write_to_csv()


def ngo_row_scrape(row):
    """
    DESCRIPTION: takes in a table row object, unpacks the data, assembled ngo
                 dictionary to store the data, appends to ngos list
    INPUT: table row object representing information for ngo
    """
    # dictionary to store ngo information
    ngo = {}
    ngo_info = row.find_all("td")

    # check if row data is valid
    if ngo_info is not None and len(ngo_info) > 0:
        _, ngo_name, ngo_descr, ngo_URL, ngo_email, _ = row.find_all("td")
        ngo["name"] = ngo_name.text.lstrip()
        ngo["description"] = ngo_descr.text.lstrip()
        # check for empty URL
        if ngo_URL.a is not None:
            ngo["URL"] = ngo_URL.a.get("href")
        # read email from website if possible
        ngo["email"] = format_ngo_email(ngo_email.text)
    # append ngo dictionary to list of ngos
    ngos.append(ngo)


def format_ngo_email(email):
    """
    DESCRIPTION: takes in ngo email read from website and formats it properly,
                 returns empty string if no email can be read
    INPUT: string email read from website
    OUTPUT: properly formatted email string to store
    """
    if "requested" not in email:
        ngo_email = email.lstrip().replace(" at ", "@")
        return ngo_email

    return ""


def write_to_csv():
    """
    DESCRIPTION: Writes everything stored in ngos list into a csv file
    """
    # write to csv to check output
    keys = ["name", "description", "URL", "email"]
    with open("thai_ngos.csv", "w") as w:
        dict_writer = csv.DictWriter(w, keys)
        dict_writer.writeheader()
        dict_writer.writerows(ngos)
