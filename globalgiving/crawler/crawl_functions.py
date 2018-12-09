from googlesearch import search
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.parse import urlparse
import requests
from globalgiving.crawler.resources.address_keywords import address_keywords
from globalgiving.crawler.resources.country_codes import country_codes
from globalgiving.crawler.rank import (
    count_phone_numbers,
    count_addresses,
    count_ngo_related_words,
    get_composite_score,
)

# dictionary that maps directory url to rank_info for one website
url_rank = {}


# dictionary template that stores all the ranking information for one directory
rank_info = {}
"""
{
    'num_links': (number of links),
    'num_subpages': (number of subpages)
    'num_addresses': (number of addresses)
    'num_phone_numbers': (number of phone numbers)
    'num_word_ngo' : (number of times word "ngo", "directory", or "nonprofit" appears on website)
    'num_word_directory': (number of times word "directory appears on website)
    'composite_score': (composite score for website)
    'page_or_dir': (boolean to indicate whether we think URL is ngo page or ngo directory)
}
"""
country_name = ""
ngo_type_name = ""


def rank_all(country):
    """
    Goes through all the urls in the url_rank dictionaryn and ranks them 
    Returns a dictionary of ngo directory url mapped to ranking information
    """
    country_name = country.title()
    for url, _ in url_rank.items():
        rank_page(url)
    return url_rank


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
    # print(subpages)

    # get all visible text from all subpages
    for subpage in subpages:
        all_visible_text += get_all_visible_text(subpage)
        # add a space to make sure text doesnt get jumbled together
        all_visible_text += " "

    # perform webpage analysis on all_visible_text HERE, update rank_info
    # rank_info["url"] = url
    rank_info["num_phone_numbers"] = count_phone_numbers(country_name, all_visible_text)
    rank_info["num_addresses"] = count_addresses(all_visible_text)
    rank_info["num_subpages"] = str(len(subpages))
    rank_info["num_word_ngo"] = str(count_ngo_related_words(all_visible_text))
    rank_info["composite_score"] = str(get_composite_score(rank_info))

    # count_ngos

    print("     Has " + str(rank_info["num_phone_numbers"]) + " phone numbers")
    print("     Has " + str(rank_info["num_addresses"]) + " addresses")
    print("     Has " + str(rank_info["num_subpages"]) + " subpages")
    print(
        "     Has "
        + str(rank_info["num_word_ngo"])
        + " appearances of ngo directory related words"
    )
    print("     Composite Score " + rank_info["composite_score"])

    url_rank[url] = rank_info.copy()
    print(url)
    print(url_rank[url])


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
    visible_text = " ".join(t.strip() for t in visible_texts)

    # print(visible_text)

    return visible_text


def tag_visible(element):
    """
    DESCRIPTION: determines if html tag is visible or not
    INPUT: element --- html tag
    OUTPUT: boolean indicating whether tag is visible or not
    """
    if element.parent.name in [
        "style",
        "script",
        "head",
        "title",
        "meta",
        "[document]",
    ]:
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
    print("Fecthing subpages for " + url)

    subpages = []
    valid_subpages = []

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    # get all URL links on homepage
    anchors = soup.findAll("a", href=True)
    links = [anchor["href"] for anchor in anchors]
    """
    Note that homepage url could be e.g. "https://care.ca/directory" due to
    google search not taking us to true homepage
    Need to remove "/directory" for true homepage url

    Three types of links that can be found
    1) relative links for subpages (e.g. /about-us/mission)
    2) absolute links for subpages (e.g. https://care.ca/about-us/mission)
    3) irrevelant external absolute link (e.g. https://mcafee.com/blahblahblah)
    """
    # home_url_length = len(home_url)
    # consider case 1) and 2) for subpage links, discard case 3)
    for link in links:
        # discard case 3)
        if link[:1] != "/" and link[: len(url)] != url:
            # print("LINK IS NOT SUBPAGE: " + link)
            continue
        # case 2)
        if link[: len(url)] == url:
            subpages.append(link)
        # case 1)
        if link[:1] == "/":
            subpages.append(url + link)
            subpages.append(url + link)

    # remove duplicates in valid_subpages
    subpages = list(set(subpages))

    # remove faulty subpage links
    for link in subpages:
        # try to access subpage link
        try:
            r = requests.get(str(link))
            if r.status_code != 404:
                valid_subpages.append(link)
        except KeyboardInterrupt:
            break
        except:
            continue
    return valid_subpages
