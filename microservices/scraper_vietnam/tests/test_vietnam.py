from .scraper_vietnam.scraper import get_page_data


def test():
    assert len(get_page_data()) >= 1
