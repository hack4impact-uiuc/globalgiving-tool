from scraper_australia.src.scraper import get_page_data, parse_page, get_test_data


def testGetPageData():
    assert len(get_page_data()) >= 1


def testgetOne():
    nonprofit = get_test_data()
    assert nonprofit["country"] == "Australia"
    assert nonprofit["name"] == "CARE Australia"


def testParsePage():
    webpage = "http://www.findouter.com/Oceania/Australia/Society-and-Culture/Non-Governmental-Organisations/1"
    assert len(parse_page(webpage)) >= 1
