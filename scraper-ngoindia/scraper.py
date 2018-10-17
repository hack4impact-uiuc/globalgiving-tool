from bs4 import BeautifulSoup
import requests

def get_page_data():
    # Specify url to scrape from
    ngo_content_list = []
    target_url = requests.get("https://ngosindia.com/ngos-of-india/")
    page_data = BeautifulSoup(target_url.content, "html.parser")
    state_list = page_data.find_all(attrs={'class': 'textwidget'})[1].find_all('a',href=True)
    #go through each state (check if states is empty)
    for state in state_list:
        #these states do not have NGO information listed on this website
        if "Delhi" in state or "Daman and Diu" in state or "Haryana" in state:
            continue
        state_url = requests.get(state['href'])
        #check that the page_data is in the correct format for getting the list
        state_page_data = BeautifulSoup(state_url.content,"html.parser")
        has_ngo_data = state_page_data.find_all(attrs={'class': 'ngo-layout-cell'})
        if has_ngo_data:
            list = has_ngo_data[1].find_all('a',href=True)
            if list:
                if "NGOs" not in list[0]:
                    get_ngo_page_fromngos(list, ngo_content_list)
                else:
                    get_ngo_page_fromcounty(list, ngo_content_list)
        else:
            continue

    return ngo_content_list

def get_ngo_data(ngo_url,ngo_content_list):
    #replace with url
    url = requests.get(ngo_url)
    page_data = BeautifulSoup(url.content, "html.parser")
    ngo_name = page_data.find_all(attrs={'class': 'ngo-postheader entry-title'})
    contents = page_data.find_all(attrs={'class': 'ngo-postcontent'})
    #contents includes data regarding NGO name, address, contact information, & mission statement
    compile_information(ngo_name,contents,ngo_content_list)


def get_ngo_page_fromngos(ngo_list,ngo_content_list):
    #return ngo_list
    for ngo in ngo_list:
        ngo_url = requests.get(ngo['href'])
        return ngo_url
        get_ngo_data(ngo_url,ngo_content_list)

def get_ngo_page_fromcounty(county_list,ngo_content_list):
    #go through each county
    for county in county_list:
        county_url = requests.get(county['href'])
        county_page_data = BeautifulSoup(county_url.content,"html.parser")
        ngo_list = county_page_data.find_all(attrs={'class': 'ngo-postcontent'})
        get_ngo_page_fromngos(ngo_list,ngo_content_list)

#return ngo_dict
def compile_information(ngo_name,contents,ngo_content_list):
    ngo_dict = {}
    #seperate neccesary information (phone,email,address,etc.)
    ngo_dict["Name"] = ngo_name
    content = str(contents[1]).split("\n")
    for item in content:
        if "Add" in item:
            ngo_dict["Address"] = item
        if "Tel" in item:
            ngo_dict["Telephone"] = item
        if "Mobile" in item:
            ngo_dict["Mobile"] = item
        if "Email" in item:
            ngo_dict["Email"] = item
        if "Website" in item:
            ngo_dict["Website"] = item
        if "Contact" in item:
            ngo_dict["Point of Contact"] = item
        if "Purpose" in item:
            ngo_dict["Purpose"] = item
        if "Aim/Objective/Mission" in item:
            ngo_dict["Mission"] = item

    ngo_content_list.append(dict)
