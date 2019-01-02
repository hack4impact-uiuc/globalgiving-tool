from scraper_hati_malaysia.src.scraper import scrape


def test():
    assert len(scrape(one=True)) >= 1
