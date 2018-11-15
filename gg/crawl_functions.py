from googlesearch import search
from bs4 import BeautifulSoup
import requests

# dictionary that maps directory url to rank_info for one website
url_rank = {}
'''
{
    URL: rank_info
}
'''
# dictionary template that stores all the ranking information for one directory
rank_info = {}
'''
{
    'num_links': (number of links),
    'num_subpages': (number of subpages)
    'num_addresses': (number of addresses)
    'num_phone_numbers': (number of phone numbers)
}
'''

#rank all the websites within url_rank dictionary
def rank_all():
    for url,_ in url_rank.items():
        rank_page(url)
    

        

#rank directory website given by url
def rank_page(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    #find all links on website
    dir_links = soup.find_all("a")
    print(dir_links)
