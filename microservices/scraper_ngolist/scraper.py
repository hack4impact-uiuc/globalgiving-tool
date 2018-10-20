from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import csv

baseurl = "https://www.thengolist.com/"


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


def basepage_scrape():
    """
    DESCRIPTION: scrapes the homepage, gets all the
                 links to country-specific pages
    """
    page = requests.get(baseurl)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # get the region list item
    region_title = soup.find("li", {"id": "pg383366003599184948"})

    region_country_ul = region_title.findChildren("ul")

    regions = region_country_ul[0]
    countries = region_country_ul[1:]
    
    #region_links = [tag.findChildren("a")["href"] for tag in regions]
    #countries_links = [tag.findChildren("a")["href"] for tag in countries]

    return regions



def write_to_csv():
    """
    DESCRIPTION: Writes everything stored in ngos list into a csv file
    """
    # write to csv to check output
    keys = ["name", "description", "URL", "email"]
    with open("thai_ngos.csv", "w") as w:
        dict_writer = csv.DictWriter(w, keys)
        dict_writer.writeheader()
        dict_writer.writerows(ngos)
