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
    
    
    # visible_text = get_all_visible_text(url)
    subpages = find_subpages(url)
    
    

# gets all the visible text of homepage and subpages one level deep
def get_all_visible_text(url):

    subpages = get_all_visible_text(url)

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    visible_text =  " ".join(t.strip() for t in visible_texts)

    print(visible_text)

    return visible_text

# returns True for visible tag, returns False otherwise
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# returns a list of all subpages of the URL
def find_subpages(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    anchors = soup.findAll('a', href = True)
    links = [anchor['href'] for anchor in anchors]
    valid_subpages = []
    # test to see if link is subpage link
    for link in links:
        print("!!")
        try:
            requests.get(str(url + link))
        except:
            continue
        valid_subpages.append(str(url+link))

    print("VALID SUBPAGES:")
    print(valid_subpages)

    return valid_subpages
