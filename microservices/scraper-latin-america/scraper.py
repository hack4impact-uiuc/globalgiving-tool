from bs4 import BeautifulSoup
import requests
import json


def get_page_data():
    # Specify url to scrape from
    target_url = requests.get(
        "http://www.oas.org/en/ser/dia/civil_society/registry.shtml"
    )
    page_data = BeautifulSoup(target_url.content, "html.parser")

    # retreive the html table which holds all the information
    table = page_data.body.find("table", {"id": "AutoNumber8"})
    # get list of all entries in the table
    table_rows = table.find_all("tr")
    ngoInformation = []
    for entry in table_rows:
        ngoDict = {}
        ngo_link = entry.find("a", {"target": "_blank"})
        if ngo_link is not None:
            ngo_link = ngo_link.get("href")
        else:
            continue
        if entry.find("font", {"color": "#004b99"}) is not None:
            ngo_name = entry.find("font", {"color": "#004b99"}).contents[0]
        else:
            continue
        ngo_info = entry.find("div", {"align": "left"})
        if ngo_info is None:
            continue
        ngo_email = ngo_info.find("a").get("href").replace("mailto:", "")
        ngo_info = str(ngo_info.contents[0]).split("<br/>")
        ngoDict["Name"] = str(ngo_name)
        ngoDict["Website"] = str(ngo_link)
        ngoDict["Email"] = str(ngo_email)
        ngoDict["info"] = str(ngo_info)
        ngoInformation.append(ngoDict)

    return json.dumps(ngoInformation, indent=4, separators=(",", ": "))
