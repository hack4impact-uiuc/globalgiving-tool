from bs4 import BeautifulSoup
import requests
import json

website = "http://www.findouter.com/Oceania/Australia/Society-and-Culture/Non-Governmental-Organisations/"


def helper(webpage, ret):
    target_url = requests.get(webpage)
    page_data = BeautifulSoup(target_url.content, "html.parser")
    contents = page_data.find("div", {"class": "container"})
    print(type(contents))
    return contents
    contents = contents.find_all("p")
    for ngo in contents:
        d = {}
        ngo = str(ngo).split("<br/>\n")
        roy_made_me_do_this(ngo, d)
        ret.append(d)
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
    ret = []
    for i in range(1,7):
        webpage = website + str(i)
        return helper(webpage, ret)
    return json.dumps(ret)
