from bs4 import BeautifulSoup
from .models.organization import Org
import requests
import json

ngo_content_list = []


def get_one_nonprofit():
    url = "https://nposindia.com/amazing-life-ministries-andaman-nicobar-islands/"
    return get_ngo_data(url)

def get_page_data():
    # Specify url to scrape from
    target_url = requests.get("https://ngosindia.com/ngos-of-india/")
    page_data = BeautifulSoup(target_url.content, "html.parser")
    state_list = page_data.find_all(attrs={"class": "textwidget"})[1].find_all(
        "a", href=True
    )
    # go through each state (check if states is empty)
    ngo_urls = []
    for state in state_list[:15]:
        #     # these states do not have NGO information listed on this website
        if "Delhi" in state or "Daman and Diu" in state or "Haryana" in state:
            continue
        state_url = requests.get(state["href"])
    #     # check that the page_data is in the correct format for getting the list
        state_page_data = BeautifulSoup(state_url.content, "html.parser")
        has_ngo_data = state_page_data.find_all(
            attrs={"class": "ngo-layout-cell"})
        if has_ngo_data:
            ngo_list = has_ngo_data[1].find_all("a", href=True)
            if (len(ngo_list) > 0 and "NGOs" in str(ngo_list[0])):
                ngo_urls += ngo_list
    urls = []
    for ngo in ngo_urls:
        if "nposindia.com" in ngo["href"]:
            urls += [ngo["href"]]
    return {"pages": len(urls), "urls": urls}


def get_ngo_data(ngo_url):
    ngo_url = requests.get(ngo_url)
    # replace with url
    page_data = BeautifulSoup(ngo_url.content, "html.parser")
    # ngo_name = page_data.find_all(
    #     attrs={"class": "ngo-postheader entry-title"})
    # print(page_data.title)
    contents = page_data.find_all(attrs={"class": "npos-postcontent clearfix"})
    # print(contents)
    # # contents includes data regarding NGO name, address, contact information, & mission statement
    return compile_information(str(page_data.title), contents)


# def get_ngo_page_fromngos(ngo_list):
#     for ngo in ngo_list:
#         ngo_url = requests.get(ngo["href"])
#         get_ngo_data(ngo_url)


# def get_ngo_page_fromcounty(county_list):
#     # go through each county
#     for county in county_list:
#         county_url = requests.get(county["href"])
#         county_page_data = BeautifulSoup(county_url.content, "html.parser")
#         if len(county_page_data.find_all(attrs={"class": "ngo-postcontent"})) >= 1:
#             ngo_list = county_page_data.find_all(attrs={"class": "ngo-postcontent"})[
#                 0
#             ].find_all("a", href=True)
#         else:
#             continue
#         get_ngo_page_fromngos(ngo_list)


# return ngo_dict
def compile_information(ngo_name, contents):
    global ngo_content_list
    ngo_dict = {}
    # seperate neccesary information (phone,email,address,etc.)
    ngo_dict["Name"] = str(
        ngo_name[ngo_name.find(">") + 1: ngo_name.find("<", 2)])
    # print(ngo_name)
    print(str(ngo_name[ngo_name.find(">") + 1: ngo_name.find("<", 2)]))
    if len(contents) > 1:
        content = str(contents[1]).split("\n")
        # Remove additional text in string like ("Add:","Tel:",etc.)
        add = None
        tel = None
        email = None
        website = None
        contact = None
        description = None
        for item in content:
            if "Add" in item:
                add = item.replace("Add", "").replace(":", "")
            if "Tel" in item:
                tel = item.replace("Tel", "").replace(":", "")
            # if "Mobile" in item:
            #     ngo_dict["Mobile"] = item.replace("Mobile", "").replace(":", "")
            if "Email" in item:
                email = item.replace("Email", "").replace(":", "")
            if "Website" in item:
                website = item.replace("Website", "").replace(":", "")
            if "Contact" in item:
                contact = item.replace("Contact", "").replace(":", "")
            if "Purpose" in item:
                if description is not None:
                    description += item.replace("Purpose", "").replace(":", "")
                else:
                    description = item.replace("Purpose", "").replace(":", "")
            if "Aim/Objective/Mission" in item:
                if description is not None:
                    description += item.replace("Aim/Objective/Mission", "").replace(
                        ":", ""
                    )
                else:
                    description = item.replace("Aim/Objective/Mission", "").replace(
                        ":", ""
                    )

        org = Org(
            name=ngo_dict["Name"],
            address=add,
            phone=tel,
            email=email,
            url=website,
            contact=contact,
            description=description,
            country="India",
        ).to_json()
        # print(org)
        # print(ngo_name)
        return org
