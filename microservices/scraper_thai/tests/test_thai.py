from scraper_thai.src.scraper import basepage_scrape, format_ngo_email, get_one_ngo


def test():
    assert len(basepage_scrape()) >= 1


def test_formatting_email():
    assert format_ngo_email("info at dogrescuecenter.org") == "info@dogrescuecenter.org"


def test_getting_one_ngo():
    assert get_one_ngo()["name"] == "Animal Sanctuary "
    assert get_one_ngo()["country"] == "Thailand"
