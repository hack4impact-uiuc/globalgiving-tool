from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import csv

base_url = "https://www.thengolist.com"


# list of dictionaries to store ngo information
ngos = []
ngos_store_keys = [
    "ngo_name",
    "ngo_URL",
    "phone_num",
    "email",
    "registration_id",
    "year_established",
    "description",
    "country"
    "facebook"
]

#dictionary of key:value pairs of "region": [list of country links]
region_country_links_dict = {}


def basepage_scrape():
    """
    DESCRIPTION: scrapes the homepage, gets all the links to country pages
                 and puts them in a dictionary that maps region to country links
    """
    page = requests.get(base_url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # get "the list" menu item from menubar
    region_title = soup.find("li", {"id": "pg383366003599184948"})

    # find all ul's under "the list"
    region_country_ul = region_title.findChildren("ul")

    # separate ul list into just countries_uls list
    countries_uls = region_country_ul[1:]

    # store all country links in list of lists
    countries_links = [ul.findChildren("a") for ul in countries_uls]
    
    # assemble region to country links dictionary mapping
    region_country_links_dict = {
        "South-America": countries_links[0],
        "Central-America": countries_links[1],
        "Asia": countries_links[2]
    }

    # scrape South-America country pages:
    for country in region_country_links_dict["South-America"]:
        country_link = country["href"]
        country_page_scrape(country_link)

    # store scraped data into csv
    write_to_csv()

    return region_country_links_dict["South-America"]


def country_page_scrape(country_link):
    """
    DESCRIPTION: scrapes the country-specific ngo page
    INPUT: country relative link scraped by basepage_scrape()
    """
    # assemble absolute URL for country-specific page
    country_url = base_url + country_link

    # get soup object
    page = requests.get(country_url)
    soup = BeautifulSoup(page.content, "html.parser")

    # get the NGO tables
    ngo_tables = soup.find_all("table", class_="wsite-multicol-table")

    # discard first two tables (general information about country)
    ngo_tables = ngo_tables[2:]

    for ngo_table in ngo_tables:
        ngo_table_scrape(ngo_table)

    return ngo_tables


def ngo_table_scrape(ngo_table):
    """
    DESCRIPTION: scrapes one table of ngos on country-specific ngo page
                 note: on this website, one table contains only one table row
    INPUT: ngo table scraped from country-specific ngo page
    """

    # get all three tds in one ngo_table
    tds = ngo_table.find_all("td")

    # scrape ngo information from td
    for td in tds:
        divs = td.find_all("div")
        # only scrape for valid td formats
        if len(divs) > 5:
            ngo_td_scrape(td)


def ngo_td_scrape(td):
    """
    DESCRIPTION: scrapes one ngo td representing one ngo on country-specific ngo page
    INPUT: ngo td scraped by ngo_table_scrape() on country-specific ngo page
    """
    ngo_name_div, ngo_descr_div, ngo_contact_div = td.find_all("div", {"class": "paragraph"})


    #take out strong tags text in ngo name
    # for i, strong in enumerate(ngo_name_div('strong')):
    #     if i != 0:
    #         strong.decompose()
    ngo_name_font_tags = ngo_name_div.find_all("font")
    ngo_name = ngo_name_font_tags[1].text

    #take out strong tags text in ngo description
    for strong in ngo_descr_div('strong'):
        strong.decompose()
    ngo_descr = ngo_descr_div.get_text()

    ngo_contact_a_tags = ngo_contact_div.find_all("a")

    ngo_URL = ngo_contact_a_tags[0]['href']
    ngo_facebook = ngo_contact_a_tags[1]['href']

    print(ngo_URL)
    print(ngo_facebook)


def email_format(email_string):
    """
    DESCRIPTION: formats emails read from webpage properly
    INPUT: email string denoting email read from webpage
    OUTPUT: properly formatted email string ready for store
    """

    return ""


def write_to_csv():
    """
    DESCRIPTION: Writes everything stored in ngos list into a csv file
    """
    # write to csv to check output
    keys = ngos_store_keys
    with open("ngo_list.csv", "w") as w:
        dict_writer = csv.DictWriter(w, keys)
        dict_writer.writeheader()
        dict_writer.writerows(ngos)
