from scraper_uganda.src.scraper import scrape_page, get_page_data


def test():
    assert len(get_page_data()) >= 1


def test_ngo_parser():
    ngo = get_page_data()[10]
    assert ngo["name"] == "Action Group for Health Human Rights and HIV/AIDS Uganda"
    assert ngo["country"] == "Uganda"
