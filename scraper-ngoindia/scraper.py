from bs4 import BeautifulSoup
import requests

def get_page_data():
    # Specify url to scrape from
    target_url = requests.get("https://ngosindia.com/ngos-of-india/")
    page_data = BeautifulSoup(target_url.content, "html.parser")
    state_list = page_data.find_all(attrs={'class': 'textwidget'})[1].find_all('a',href=True)
    #go through each state (check if states is empty)
    for state in state_list:
        state_url = requests.get(state['href'])
        state_page_data = BeautifulSoup(state_url.content,"html.parser")
        county_list = state_page_data.find_all(attrs={'class': 'ngo-layout-cell'})[1].find_all('a',href=True)
    #go through each county
        for county in county_list:
            county_url = requests.get(county['href'])
            county_page_data = BeautifulSoup(county_url.content,"html.parser")
            ngo_list = county_page_data.find_all(attrs={'class': 'ngo-postcontent'})
    #go through each NGO (call get_specific_page_data) for each NGO
            for ngo in ngo_list:
                ngo_url = requests.get(ngo['href'])
                get_specific_page_data(ngo_url)

def get_specific_page_data(ngo_url):
    #replace with url
    page_data = BeautifulSoup(ngo_url.content, "html.parser")
    ngo_name = page_data.find_all(attrs={'class': 'ngo-postheader'})
    contents = page_data.find_all(attrs={'class': 'ngo-postcontent'})
    contents[0] = ngo_name
    #contents includes data regarding NGO name, address, contact information, & mission statement
    print(contents)
