from bs4 import BeautifulSoup
import requests
import json

website = "http://www.findouter.com/Oceania/Australia/Society-and-Culture/Non-Governmental-Organisations/"


def helper(webpage):
    list_of_ds = []
    target_url = requests.get(webpage)
    page_data = BeautifulSoup(target_url.content, "html.parser")
    contents = page_data.find("div", {"class": "container"})
    title = True
    for ngo in str(contents).split('<div class="firstline">\n'):
        d = {}
        if title:
            title = False
            continue
        # print(ngo)
        for line in ngo.split('\n'):
            if line[:23] == '<span class="sitename">':
                line = line.split('>')
                d["Website"] = line[1].split('"')[1]
                d["Name"] = line[2][:-3]
            elif line[:20] == '<span class="phone">':
                d["Telephone"] = line[25:40]
            elif line[:22] == '<span class="address">':
                line = line.split('>')
                d["Address"] = line[1][:-6]
            elif line[:25] == '<div class="description">':
                line = line.split('>')
                d["Description"] = line[1][:-5]
        list_of_ds.append(d)
    return list_of_ds

def get_page_data():
    ret = []
    for i in range(1,7):
        webpage = website + str(i)
        ret.extend(helper(webpage))
    return json.dumps(ret)
