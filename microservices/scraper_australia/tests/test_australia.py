from scraper_australia.src.scraper import get_page_data, parse_page, get_one_nonprofit


def testGetPageData():
    assert len(get_page_data()) >= 1


def testgetOne():
    get_one_nonprofit()
    assert (get_one_nonprofit())["country"] == "Australia"
    assert (get_one_nonprofit())["name"] == "CARE Australia"


def testParsePage():
    webpage = "http://www.findouter.com/Oceania/Australia/Society-and-Culture/Non-Governmental-Organisations/1"
    assert len(parse_page(webpage)) >= 1
