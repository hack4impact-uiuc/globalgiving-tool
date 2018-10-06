from bs4 import BeautifulSoup
import requests

def get_page_data():
    # Specify url to scrape from
    target_url = requests.get("https://ngosindia.com/ngos-of-india/")
    page_data = BeautifulSoup(target_url.content, "html.parser")
    state_list = page_data.find_all(attrs={'class': 'textwidget'})[1].find_all('a')
    #go through each state
    #for i in state_list:
        #extract link, get page_data of this url

    #go through each county
    #go through each NGO (call get_specific_page_data) for each NGO

def get_specific_page_data(url):
    #replace with url
    target_url = requests.get("https://andaman-nicobar.ngosindia.com/fire-gospel-mission-south-andaman-2/")
    page_data = BeautifulSoup(target_url.content, "html.parser")
    ngo_name = page_data.find_all(attrs={'class': 'ngo-postheader'})
    contents = page_data.find_all(attrs={'class': 'ngo-postcontent'})
    contents[0] = ngo_name
    #contents includes data regarding NGO name, address, contact information, & mission statement
    return contents
