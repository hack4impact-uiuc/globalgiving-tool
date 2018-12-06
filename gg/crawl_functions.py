from googlesearch import search
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import urlparse
import requests

# dictionary that maps directory url to rank_info for one website
url_rank = {}
'''
{
    URL: rank_info dict
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
    'num_word_ngo' : (number of times word "ngo" appears on website)
    'num_word_directory': (number of times word "directory appears on website)
    'composite_score': (composite score for website)
    'page_or_dir': (boolean to indicate whether we think URL is ngo page or ngo directory)
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
    INPUT: url --- absolute URL to NGO website
    OUTPUT: none
    BEHAVIOR: expect url_rank to now contain dictionary of rank_info as value. This
              dictionary stores information pertinent to ranking as well as composite rank score
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    all_visible_text = get_all_visible_text(url)
    
    # get all subpages
    subpages = find_subpages(url)

    # get all visible text from all subpages
    for subpage in subpages:
        all_visible_text += get_all_visible_text(subpage)
        # add a space to make sure text doesnt get jumbled together
        all_visible_text += " "
    

    # perform webpage analysis on all_visible_text HERE, update rank_info
    
    # print(all_visible_text)


    # get composite_score
    # composite_score = get_composite_score(url_rank[url])
    #store composite_score
    # url_rank[url]['composite_score'] = composite_score
    
def count_phone_numbers(visible_text):
    """
    DESCRIPTION: counts number of phone numbers occuredd on NGO website
    INPUT: visible_text --- all the visible text of NGO website homepage and subpages
    OUTPUT: integer number of phone numbers found in visible text
    """
    pass

def count_ngos_and_directory(visible_text):
    """
    DESCRIPTION: counts number of instances of 'ngo' and 'directory'
    INPUT: visible_text --- all the visible text of NGO website homepage and subpages
    OUTPUT: integer number of instances of 'ngo' and 'directory'
    """
    visible_text = visible_text.lower()
    return visible_text.count('ngo'), visible_text.count('directory')

def get_composite_score(rank_info):
    """
    DESCRIPTION: ranks the NGO website specified by url
    INPUT: url --- URL to NGO website
    OUTPUT: none
    BEHAVIOR: expect url_rank to now contain dictionary of rank_info as value. This
              dictionary stores information pertinent to ranking as well as composite rank score
    """
    #heuristic can be altered here:
    # composite_score = rank_info['num_phone_numbers']

    # return composite_score
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
    INPUT: url --- absolute URL to NGO website
    OUTPUT: string of all visible text on NGO website
    """

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")


    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    visible_text =  " ".join(t.strip() for t in visible_texts)

    # print(visible_text)

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
    DESCRIPTION: scrapes website homepage for all subpages
    INPUT: url --- absolute URL denoting ngo website homepage
    OUTPUT: list of all subpage URLs
    """

    #get the domain url from homepage url
    parsed_uri = urlparse(url)
    home_url = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    print("STRIPPED URL:")
    print(home_url)

    subpages = []
    valid_subpages = []

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # get all URL links on homepage
    anchors = soup.findAll('a', href = True)
    links = [anchor['href'] for anchor in anchors]
    '''
    Note that homepage url could be e.g. "https://care.ca/directory" due to
    google search not taking us to true homepage
    Need to remove "/directory" for true homepage url

    Three types of links that can be found
    1) relative links for subpages (e.g. /about-us/mission)
    2) absolute links for subpages (e.g. https://care.ca/about-us/mission)
    3) irrevelant external absolute link (e.g. https://mcafee.com/blahblahblah)
    '''
    home_url_length = len(home_url)
    # consider case 1) and 2) for subpage links, discard case 3)
    for link in links:
        # discard case 3)
        if (link[:1] != '/' and link[:home_url_length] != home_url):
            print("LINK IS NOT SUBPAGE: "+ link)
            continue
        # case 2)
        if (link[:home_url_length] == home_url):
            subpages.append(link)
        # case 1)
        if (link[:1] == '/'):
            subpages.append(url + link)
            subpages.append(home_url + link)

    # remove duplicates in valid_subpages
    subpages = list(set(subpages))

    # remove faulty subpage links
    for link in subpages:
        # try to access subpage link
        try:
            r = requests.get(str(link))
            print(r.status_code)
            if (r.status_code != 404):
                valid_subpages.append(link)
        except:
            print("exception caught!")
            continue


    print("VALID SUBPAGES: " + str(len(valid_subpages)))
    print(valid_subpages)

    # output all subpage links to text file for easier examination
    f = open('subpages.txt','w')
    for valid_subpage in valid_subpages:
        f.write(valid_subpage + "\n")
    f.close()

    return valid_subpages

#-----------------------------------------------------------------------------------------------
#------------------------------FUNCTIONS TO GET VISIBLE TEXT-------------s----------------------   
#-----------------------------------------------------------------------------------------------
