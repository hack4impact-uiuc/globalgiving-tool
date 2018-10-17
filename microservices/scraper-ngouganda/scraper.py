from bs4 import BeautifulSoup
import requests
import json

website = "https://informationcradle.com/africa/list-of-ngos-in-uganda/"


def roy_made_me_do_this(ngo, d):
    for line in ngo:
        if line[-4:] == "</p>":
            line = line[:-4]
        if line[:3] == "<p>":
            d["Name"] = line[11:-9]
        elif line[:7] == "P.O.Box":
            d["P.O. Box"] = line[8:]
        elif line[:4] == "www.":
            d["Website"] = line
        elif line[:8] == "Category":
            d["Category"] = line[10:]
        elif line[:16] == "Physical Address":
            d["Physical Address"] = line[16:]
        elif line[:9] == "Telephone":
            d["Telephone"] = line[11:]
        elif line[:6] == "E-mail":
            d["E-mail"] = line[8:]
        elif line[:14] == "Contact Person":
            d["Contact Person"] = line[16:]
        else:
            d["Description"] = line


def get_page_data():
    # Specify url to scrape from
    ret = []
    target_url = requests.get(website)
    page_data = BeautifulSoup(target_url.content, "html.parser")
    contents = page_data.find("div", {"class": "entry-content"})
    contents = contents.find_all("p")
    for ngo in contents:
        d = {}
        ngo = str(ngo).split("<br/>\n")
        roy_made_me_do_this(ngo, d)
        ret.append(d)
    return json.dumps(ret)
