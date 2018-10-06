from bs4 import BeautifulSoup
import requests

thaiwebsite_NGOs = []
baseurl = "http://www.thaiwebsites.com/social.asp"


def basepage_scrape():
    page = requests.get(baseurl)
    soup = BeautifulSoup(page.content, "html.parser")
    thaiwebsites_NGOs = soup.find_all('a')
    # print(soup)
    print(thaiwebsites_NGOs, endl = '\n')

def NGOpage_scrape():
    pass
