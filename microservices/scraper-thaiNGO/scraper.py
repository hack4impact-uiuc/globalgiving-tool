from bs4 import BeautifulSoup
import requests

baseurl = "http://www.thaiwebsites.com/social.asp"

ngo_names = []
ngo_URLs = []

"""
list of dictionaries to store ngo information
ngos = {
    ngo_name: "",
    ngo_URLs: "",
    phone_num: "",
    email: "",
    registration_id: ""
}
"""
ngos = []

"""
DESCRIPTION: scrapes the directory for Thai NGOs
             
"""
def basepage_scrape():
    page = requests.get(baseurl)
    soup = BeautifulSoup(page.content, "html.parser")
    #find all links that have class="link14"
    websites_a_tags = soup.find_all("a", {"class": "link14"})

    ngo_names = [tag.text for tag in websites_a_tags]
    ngo_URLs = [tag['href'] for tag in websites_a_tags]
    
    print(ngo_names)
    print(ngo_URLs)
    print(len(ngo_names))

    return websites_a_tags


"""
DESCRIPTION: scrapes a specific Thai NGO website
INPUT: takes in URL to specific Thai NGO Website
"""
def ngo_page_scrape(url):

    pass
