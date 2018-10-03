from bs4 import BeautifulSoup
import requests

def get_page_data():
    # Specify url to scrape from
    target_url = requests.get("https://ngosindia.com/ngos-of-india/")
    page_data = BeautifulSoup(target_url.content, "html.parser")
    return page_data.body.contents

def get_specific_page_data():
    target_url = requests.get("https://andaman-nicobar.ngosindia.com/fire-gospel-mission-south-andaman-2/")
    page_data = BeautifulSoup(target_url.content, "html.parser")
    return page_data.find_all(attrs={'class': 'ngo-postcontent'})
    #return page_data.body.contents

#paragraph data: ngo-postcontent clearfix
