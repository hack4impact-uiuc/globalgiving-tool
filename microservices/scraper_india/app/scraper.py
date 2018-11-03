from bs4 import BeautifulSoup
import requests

ngo_content_list = []


def get_one_nonprofit():
    url = "https://andaman-nicobar.ngosindia.com/amazing-life-ministries-andaman-nicobar-islands/"
    ngo_url = requests.get(url)
    get_ngo_data(ngo_url)
    return {"data" : [ngo_content_list[0]] }

def get_page_data():
    # Specify url to scrape from
    target_url = requests.get("https://ngosindia.com/ngos-of-india/")
    page_data = BeautifulSoup(target_url.content, "html.parser")
    state_list = page_data.find_all(attrs={"class": "textwidget"})[1].find_all(
        "a", href=True
    )
    # go through each state (check if states is empty)
    for state in state_list:
        # these states do not have NGO information listed on this website
        if "Delhi" in state or "Daman and Diu" in state or "Haryana" in state:
            continue
        state_url = requests.get(state["href"])
        # check that the page_data is in the correct format for getting the list
        state_page_data = BeautifulSoup(state_url.content, "html.parser")
        has_ngo_data = state_page_data.find_all(attrs={"class": "ngo-layout-cell"})
        if has_ngo_data:
            list = has_ngo_data[1].find_all("a", href=True)
            if list:
                # page is at ngo-level
                if "NGOs" not in str(list[0]):
                    get_ngo_page_fromngos(list)
                else:
                    # page is at county-level
                    get_ngo_page_fromcounty(list)

    return ngo_content_list


def get_ngo_data(ngo_url):
    # replace with url
    page_data = BeautifulSoup(ngo_url.content, "html.parser")
    ngo_name = page_data.find_all(attrs={"class": "ngo-postheader entry-title"})
    contents = page_data.find_all(attrs={"class": "ngo-postcontent"})
    # contents includes data regarding NGO name, address, contact information, & mission statement
    print(str(ngo_name))
    compile_information(str(ngo_name), contents)


def get_ngo_page_fromngos(ngo_list):
    # return ngo_list
    for ngo in ngo_list:
        # print(ngo)
        ngo_url = requests.get(ngo["href"])
        # print(ngo["href"])
        get_ngo_data(ngo_url)


def get_ngo_page_fromcounty(county_list):
    # go through each county
    for county in county_list:
        county_url = requests.get(county["href"])
        county_page_data = BeautifulSoup(county_url.content, "html.parser")
        if len(county_page_data.find_all(attrs={"class": "ngo-postcontent"})) >= 1:
            ngo_list = county_page_data.find_all(attrs={"class": "ngo-postcontent"})[
                0
            ].find_all("a", href=True)
        else:
            continue
        # print("YO")
        # print(county["href"])
        # print("YO")
        get_ngo_page_fromngos(ngo_list)


# return ngo_dict
def compile_information(ngo_name, contents):
    global ngo_content_list
    ngo_dict = {}
    # seperate neccesary information (phone,email,address,etc.)
    ngo_dict["Name"] = str(ngo_name[ngo_name.find(">")+1: ngo_name.find("<", 2)])
    # print(ngo_name.substr(ngo_name.find(">")).find("<"))
    if len(contents) > 1:
        content = str(contents[1]).split("\n")
        # Remove additional text in string like ("Add:","Tel:",etc.)
        for item in content:
            if "Add" in item:
                ngo_dict["Address"] = item.replace("Add", "").replace(":", "")
            if "Tel" in item:
                ngo_dict["Telephone"] = item.replace("Tel", "").replace(":", "")
            if "Mobile" in item:
                ngo_dict["Mobile"] = item.replace("Mobile", "").replace(":", "")
            if "Email" in item:
                ngo_dict["Email"] = item.replace("Email", "").replace(":", "")
            if "Website" in item:
                ngo_dict["Website"] = item.replace("Website", "").replace(":", "")
            if "Contact" in item:
                ngo_dict["Point of Contact"] = item.replace("Contact", "").replace(
                    ":", ""
                )
            if "Purpose" in item:
                ngo_dict["Purpose"] = item.replace("Purpose", "").replace(":", "")
            if "Aim/Objective/Mission" in item:
                ngo_dict["Mission"] = item.replace("Aim/Objective/Mission", "").replace(
                    ":", ""
                )

    ngo_content_list.append(ngo_dict)
