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
    print('retreived category page links')

    ngoLinks = []  # build list of links for NGOs
    for link in catLinks:
        categoryName = link[28:-1]
        target_url = requests.get(link)
        page_data = BeautifulSoup(target_url.content, "html.parser")
        ngoContent = page_data.body.find_all('a', {'class': 'read-more'})  # we can grab the ngo links most readily from the read more buttons
        for ngoLink in ngoContent:
            ngoLinks.append(ngoLink.get('href'))
            if categoryName in ngoLink:
                ngoLinks.append(ngoLink)
    print('retreived NGO page links')
    
    # get rid of duplicate links
    ngoLinks = list(set(ngoLinks))
    print('purged duplicate links')

    # now scrape relevant information from the individual NGOs
    for ngoLink in ngoLinks:
        target_url = requests.get(ngoLink)
        page_data = BeautifulSoup(target_url.content, "html.parser")
        
        break


    return ngoLinks
