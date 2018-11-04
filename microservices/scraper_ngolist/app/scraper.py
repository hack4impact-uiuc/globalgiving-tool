from bs4 import BeautifulSoup
from requests import get
import csv
import re

base_url = "https://www.thengolist.com"


# list of dictionaries to store ngo information
ngos = []
ngos_store_keys = ["ngo_name", "description", "ngo_URL", "facebook", "email", "country"]

# dictionary of key:value pairs of "region": [list of country links]
region_country_links_dict = {}


def basepage_scrape():
    """
    DESCRIPTION: scrapes the homepage, gets all the links to country pages
                 and puts them in a dictionary that maps region to country links
    """
    page = get(base_url)
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
        "Asia": countries_links[2],
    }

    # scrape only South-America country pages:
    # other continent country pages do not contain enough useful information
    for country in region_country_links_dict["South-America"]:
        country_link = country["href"]
        country_page_scrape(country_link)

    # store scraped data into csv
    write_to_csv()

    return region_country_links_dict["South-America"]


def country_page_scrape(country_link):
    """
    DESCRIPTION: scrapes the country-specific ngo page
    INPUT: country_link - country relative link scraped by basepage_scrape()
    """
    # assemble absolute URL for country-specific page
    country_url = base_url + country_link

    # get soup object
    page = get(country_url)
    soup = BeautifulSoup(page.content, "html.parser")

    # get the NGO tables
    ngo_tables = soup.find_all("table", class_="wsite-multicol-table")

    # discard first two tables (general information about country)
    ngo_tables = ngo_tables[2:]

    for ngo_table in ngo_tables:
        # remove ".html" at end of link & "/" at beginning of link to get country name
        ngo_table_scrape(ngo_table, country_link[:-5][1:])

    return ngo_tables


def ngo_table_scrape(ngo_table, country_name):
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
            ngo_td_scrape(td, country_name)


def ngo_td_scrape(td, country_name):
    """
    DESCRIPTION: scrapes one ngo td representing one ngo on country-specific ngo page
    INPUT: ngo td scraped by ngo_table_scrape() on country-specific ngo page
    """
    # intialize all NGO information entresi
    ngo_name = ""
    ngo_descr = ""
    ngo_URL = ""
    ngo_facebook = ""
    ngo_email = ""
    ngo_country = country_name

    try:
        ngo_name_div, ngo_descr_div, ngo_contact_div = td.find_all(
            "div", {"class": "paragraph"}
        )
    except ValueError:
        print("Country could not be scraped.")
        return
    # -----------------------FIND NGO NAME-----------------------------
    ngo_name_font_tags = ngo_name_div.find_all("font", {"size": "5"})
    # ngo name's font tag either has no children or is
    # is the first child of the font tags found
    # CASE 1:
    # <font color = "#000">
    #     <font size = "5"> NAME </font>
    # </font>
    # CASE 2:
    # <font size = "5">
    #     <font color = "#000"> NAME </font>
    #     <font> DONT CARE </font>
    # </font>
    for font_tag in ngo_name_font_tags:
        if font_tag.findChild() == None:
            ngo_name = font_tag.text
            break
        else:
            ngo_name = font_tag.findChild().text
            break

    if ngo_name == "":
        print("Ngo name was not found!!")

    # -----------------------FIND NGO DESCRIPTION---------------------------
    for strong in ngo_descr_div("strong"):
        strong.decompose()
    ngo_descr = ngo_descr_div.get_text()

    # -----------------------FIND NGO CONTACT INFO-----------------------------
    ngo_contact_a_tags = ngo_contact_div.find_all("a")
    if ngo_contact_a_tags != None:
        try:
            ngo_URL = ngo_contact_a_tags[0]["href"]
        except IndexError:
            print("ngo URL could not be found!")
        try:
            ngo_facebook = ngo_contact_a_tags[1]["href"]
        except IndexError:
            print("ngo facebook could not be found!")

    ngo_contact_text = ngo_contact_div.text
    ngo_contact_text = ngo_contact_text.replace("fb:", " ")
    match = re.search(
        r"mail:[\w\. -]+\(at\)[\w\. -]+\(dot\)[\w\. -]+", ngo_contact_text
    )

    if match == None:
        print("NGO email could not be found!!")
    else:
        ngo_email = email_format(match.group())

    # assemble ngo dict
    ngo = {}
    ngo["ngo_name"] = ngo_name
    ngo["description"] = ngo_descr
    ngo["ngo_URL"] = ngo_URL
    ngo["facebook"] = ngo_facebook
    ngo["email"] = ngo_email
    ngo["country"] = ngo_country
    print(ngo)
    # append ngo dictionary to list of ngos
    ngos.append(ngo)


def email_format(email_string):
    """
    DESCRIPTION: formats emails read from webpage properly
    INPUT: email string denoting email read from webpage
    OUTPUT: properly formatted email string ready for store
    """
    ngo_email = email_string.replace("mail:", "")
    ngo_email = ngo_email.replace(" (at) ", "@")
    ngo_email = ngo_email.replace(" (dot) ", ".")
    ngo_email = ngo_email.lstrip().rstrip()

    return ngo_email


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
