from googlesearch import search
from bs4 import BeautifulSoup
from bs4.element import Comment
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
    'page_or_dir': (boolean to indicate whether URL is ngo page or ngo directory)
    'num_links': (number of links),
    'num_subpages': (number of subpages)
    'num_addresses': (number of addresses)
    'num_phone_numbers': (number of phone numbers)
    'composite_score': (composite score for website)
}
'''

#-----------------------------------------------------------------------------------------------
#-----------------------------------RANKING FUNCTIONS-------------------------------------------   
#-----------------------------------------------------------------------------------------------

def rank_all():
    """
    DESCRIPTION: goes through all the URLs in url_rank dictionary and ranks them
    INPUT: none
    OUTPUT: none
    BEHAVIOR: expect url_rank to now contain dictionaries of rank_info as values. These
              dictionaries store information pertinent to ranking as well as composite rank score
    """
    for url,_ in url_rank.items():
        rank_page(url)
    

def rank_page(url):
    """
    DESCRIPTION: ranks the NGO website specified by url
    INPUT: url --- URL to NGO website
    OUTPUT: none
    BEHAVIOR: expect url_rank to now contain dictionary of rank_info as value. This
              dictionary stores information pertinent to ranking as well as composite rank score
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    
    # visible_text = get_all_visible_text(url)
    subpages = find_subpages(url)
    

def get_composite_score(rank_info):
    """
    DESCRIPTION: ranks the NGO website specified by url
    INPUT: url --- URL to NGO website
    OUTPUT: none
    BEHAVIOR: expect url_rank to now contain dictionary of rank_info as value. This
              dictionary stores information pertinent to ranking as well as composite rank score
    """
    pass


#-----------------------------------------------------------------------------------------------
#-----------------------------------RANKING FUNCTIONS-------------------------------------------   
#-----------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------
#------------------------------FUNCTIONS TO GET VISIBLE TEXT-------------s----------------------   
#-----------------------------------------------------------------------------------------------


def get_all_visible_text(url):
    """
    DESCRIPTION: gets all the visible text of homepage and subpages one-level deep for NGO website
    INPUT: url --- URL to NGO website
    OUTPUT: string of all visible text on NGO website
    """

    subpages = get_all_visible_text(url)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")


    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    visible_text =  " ".join(t.strip() for t in visible_texts)

    print(visible_text)

    return visible_text


def tag_visible(element):
    """
    DESCRIPTION: determines if html tag is visible or not
    INPUT: element --- html tag
    OUTPUT: boolean indicating whether tag is visible or not
    """
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def find_subpages(url):
    """
    DESCRIPTION: scrapes website for all subpages
    INPUT: url --- URL denoting ngo website
    OUTPUT: list of all subpage URLs
    """

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    #
    anchors = soup.findAll('a', href = True)
    links = [anchor['href'] for anchor in anchors]
    valid_subpages = []
    # test to see if link is subpage link
    for link in links:
        if (len(link) > len(url) and link[len(url)] == url):
            valid_subpages.append(link)
        # external links cannot be subpage links
        elif (link[:4] == "http"):
            continue
        valid_subpages.append(url + link)


    # remove duplicates in valid_subpages
    valid_subpages = list(set(valid_subpages))
    for i,link in enumerate(valid_subpages):
        # try to access url + link 
        try:
            r = requests.get(str(link))
            print(r.status_code)
            if (r.status_code == 404):
                valid_subpages.pop(i)
        except:
            print("exception caught!")
            continue


    print("VALID SUBPAGES: " + str(len(valid_subpages)))
    print(valid_subpages)

    return valid_subpages

#-----------------------------------------------------------------------------------------------
#------------------------------FUNCTIONS TO GET VISIBLE TEXT-------------s----------------------   
#-----------------------------------------------------------------------------------------------


def get_external_links(url):
    pass