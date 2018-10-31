from selenium import webdriver
from bs4 import BeautifulSoup
import json


def scrape():
    # Specify url to scrape from
    source_url = "http://www.oas.org/en/ser/dia/civil_society/registry.shtml"

    table_rows = get_data_rows(source_url)

    ngoInformation = [parse_row_to_dict(table_row) for table_row in table_rows]

    return json.dumps(ngoInformation, indent=4, separators=(",", ": "))


def get_data_rows(source_url):
    """
    Gets the rows of data from the massive html table once loaded with
    PhantomJS (should switch to chrome or firefox)

    Input:
        source_url: url to scrape
    Returns:
        table_rows: the rows of the html table as a list
    """
    # set up JS driver
    driver = webdriver.PhantomJS()
    print("here2")
    driver.get(source_url)
    print("here3")
    page_data = BeautifulSoup(driver.page_source, "html.parser")

    # retreive the html table which holds all the information
    table = page_data.body.find("table", {"id": "AutoNumber8"})
    # get list of all entries in the table
    table_rows = table.find_all("tr", {"class": "even"}) + table.find_all(
        "tr", {"class": "odd"}
    ) + table.find_all("tr", {"class": "first even"})

    # check is there is data
    if table_rows is None:
        raise Exception("No data was found in the table.")

    return table_rows


def parse_row_to_dict(table_row):
    """
    Take in a row of data, then parse it into a dictionary and return this dict

    Input:
        table_row: a row from an html table
    Returns:
        ngoDict: a dictionary containing as much data as possible taken from
                 the table_row
    """

    ngoDict = {}  # diction to dump everything into

    all_links = table_row.find_all("a")
    ngo_links = []
    if all_links is not None:
        for link in all_links:
            if link.get("href") is not None:
                if link.get("href")[-4:-1] != ".doc":
                    ngo_links.append(link.get("href"))
    ngo_link = ngo_links[0]  # the ngo website is the first valid, non-doc link

    leftSide, rightSide = table_row.find_all("td")
    leftSide, rightSide = leftSide.contents, rightSide.contents

    print([leftSide, rightSide])
    return
    
    ngoDict["Name"] = str(ngo_name)
    ngoDict["Website"] = str(ngo_link)
    ngoDict["Email"] = str(ngo_email)
    ngoDict["info"] = str(ngo_info)

    # check is there is data
    if ngoDict is None:
        raise Exception("No data was found to put in the dictionary.")

    return ngoDict
