from bs4 import BeautifulSoup
import requests


def get_page_data():
    # Specify url to scrape from
    target_url = requests.get("http://www.hati.my/")
    page_data = BeautifulSoup(target_url.content, "html.parser")
    catLinks = []  # set up list accumulator for categories
    for link in page_data.find_all('a'):
        linkText = link.get('href')
        if linkText is not None:
            if 'category' in linkText:
                catLinks.append(linkText)  # get the link for the category

    ngoLinks = []  # build list of links for NGOs
    for link in catLinks:
        categoryName = link[28:-1]
        print(categoryName)
        target_url = requests.get(link)
        page_data = BeautifulSoup(target_url.content, "html.parser")
        ngoContent = page_data.find_all('a')
        for ngoLink in ngoContent:
            ngoLinks.append(ngoLink)
            #if ngoLink is not None and categoryName in ngoLink:
            #    ngoLinks.append(ngoLink)

    return ngoLinks
