from bs4 import BeautifulSoup
import requests
import json


def get_page_data():
    # Specify url to scrape from
    target_url = requests.get("http://www.hati.my/")
    page_data = BeautifulSoup(target_url.content, "html.parser")
    catLinks = []  # set up list accumulator for categories
    for link in page_data.find_all('a'):
        linkText = link.get('href')
        if linkText is not None:
            if 'category' in linkText:
                catLinks.append(linkText)  # get the link for the category
    print('retreived category page links')

    ngoLinks = []  # build list of links for NGOs
    for link in catLinks:
        categoryName = link[28:-1]
        target_url = requests.get(link)
        page_data = BeautifulSoup(target_url.content, "html.parser")
        ngoContent = page_data.body.find_all('a', {'class': 'read-more'})  # we can grab the ngo links most readily from the read more buttons
        for ngoLink in ngoContent:
            ngoLinks.append(ngoLink.get('href'))
            if categoryName in ngoLink:
                ngoLinks.append(ngoLink)
    print('retreived NGO page links')
    
    # get rid of duplicate links
    ngoLinks = list(set(ngoLinks))
    print('purged duplicate links')

    # now scrape relevant information from the individual NGOs
    ngoInformation = []  # a list which hold the dictionaries for all NGOs
    for ngoLink in ngoLinks:
        ngoDict = {}  # hold whatever information we can find
        ngoDict['Source'] = ngoLink  # mark source from where the data came
        target_url = requests.get(ngoLink)
        page_data = BeautifulSoup(target_url.content, "html.parser")
        name = page_data.body.find('h1', {'class': 'category-title'}).get_text()
        ngoDict['Name'] = name
        print(name)
        table = page_data.body.find('table', {'class': 'my_table_1'})
        description = page_data.body.find('div', {'class': 'entry post clearfix'}).find_all('p')
        description = " ".join([item.get_text() for item in description])  # join the paragraphs into one string
        ngoDict['Description'] = description
        table_body = table.find_all('tr')
        for row in table_body:
            rowData = row.find_all('td')
            if str(rowData[0].contents[0]) == "Website":
                ngoDict[str(rowData[0].contents[0])] = rowData[1].contents[0].get('href')
            elif str(rowData[0].contents[0]) == "Email address":
                ngoDict[str(rowData[0].contents[0])] = rowData[1].contents[0].get('href').replace('mailto:', '')
            else:
                ngoDict[str(rowData[0].contents[0])] = str(rowData[1].contents[0])
        # add the information to the master list
        ngoInformation.append(ngoDict)

    return json.dumps(ngoInformation)
