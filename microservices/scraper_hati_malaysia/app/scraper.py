from bs4 import BeautifulSoup
import requests
import json
from app.models.organization import Org

# import pymongo

# sets up database connection
# uri = "mongodb://aria:malkani28@ds139243.mlab.com:39243/gg-db"
# client = pymongo.MongoClient(uri)
# db = client.get_default_database()
# nonprofits = db['nonprofits']
# db.nonprofits.distinct( "Name" )


def get_cat_links(test=False):
    """
    Find the links for the subpages of each category by starting from the homepage
    of the website.
    """
    # Specify url to scrape from
    target_url = requests.get("http://www.hati.my/")
    page_data = BeautifulSoup(target_url.content, "html.parser")
    catLinks = []  # set up list accumulator for categories
    for link in page_data.find_all("a"):
        linkText = link.get("href")
        if linkText is not None:
            if "category" in linkText:  # only take links containing "category"
                catLinks.append(linkText)  # get the link for the category
                if test:
                    break
    print("retreived category page links")
    return catLinks


def get_ngo_links(catLinks, test=False):
    """
    Go to each category link and find all websites inside each.
    """
    ngoLinks = []  # build list of links for NGOs
    for link in catLinks:
        # http://www.hati.my/category/<categoryName>/
        #                             ^[28]         ^[-1]
        # link[28:-1] => <categoryName>
        # To get the category name, take substring from 28 to -1
        categoryName = link[28:-1]

        target_url = requests.get(link)
        page_data = BeautifulSoup(target_url.content, "html.parser")
        # we can grab the ngo links most readily from the read more buttons,
        # denoted by a "class"="read-more" tag
        ngoContent = page_data.body.find_all("a", {"class": "read-more"})
        for ngoLink in ngoContent:
            ngoLinks.append(ngoLink.get("href"))
            if categoryName in ngoLink:
                ngoLinks.append(ngoLink)
            if test:
                break
    print("retreived NGO page links")
    # get rid of duplicate links
    ngoLinks = list(set(ngoLinks))
    print("purged duplicate links")
    print(len(ngoLinks))
    return ngoLinks


def get_ngo_information(ngoLinks):
    """
    Visit each NGO's website and pull information.
    """
    # now scrape relevant information from the individual NGOs
    ngoInformation = []  # a list which hold the dictionaries for all NGOs
    for ngoLink in ngoLinks:
        ngoDict = {}  # hold whatever information we can find
        ngoDict["Source"] = ngoLink  # mark source from where the data came
        target_url = requests.get(ngoLink)
        page_data = BeautifulSoup(target_url.content, "html.parser")
        name = page_data.body.find("h1", {"class": "category-title"}).get_text()
        ngoDict["Name"] = name
        print(name)
        table = page_data.body.find("table", {"class": "my_table_1"})
        description = page_data.body.find(
            "div", {"class": "entry post clearfix"}
        ).find_all("p")
        description = " ".join(
            [item.get_text() for item in description]
        )  # join the paragraphs into one string
        ngoDict["Description"] = description
        table_body = table.find_all("tr")
        for row in table_body:
            field, value = row.find_all("td")
            if str(field.contents[0]) == "Website":
                ngoDict[str(field.contents[0])] = value.contents[0].get("href")
            elif str(field.contents[0]) == "Email address":
                ngoDict[str(field.contents[0])] = (
                    value.contents[0].get("href").replace("mailto:", "")
                )
            else:
                ngoDict[str(field.contents[0])] = str(value.contents[0])
        # add the information to the master list
        print(json.dumps(ngoDict, indent=4, separators=(",", ": ")))
        # adds the nonprofit to the database
        # nonprofits.insert(ngoDict)
        name = None
        email = None
        url = None
        phone = None
        registration = None
        address = None
        contact = None
        for key in ngoDict.keys():
            if key == "Name":
                name = ngoDict[key]
            if key == "Email address":
                email = ngoDict[key]
            if key == "Website":
                url = ngoDict[key]
            if key == "Phone number":
                phone = ngoDict[key]
            if key == "Registration number":
                registration = ngoDict[key]
            if key == "Address":
                address = ngoDict[key]
            if key == "Contact person":
                contact = ngoDict[key]
        ngoInformation.append(
            Org(
                name=name,
                phone=phone,
                email=email,
                address=address,
                contact=contact,
                registration=registration,
                url=url,
                description=description,
                country="Malaysia",
            ).to_json()
        )

    return ngoInformation


def scrape(one=False):
    """
    Put everything together.
    """
    ngoInformation = get_ngo_information(
        get_ngo_links(get_cat_links(test=one), test=one)
    )
    return json.dumps(ngoInformation, indent=4, separators=(",", ": "))
