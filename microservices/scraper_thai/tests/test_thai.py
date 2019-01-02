from scraper_thai.src.scraper import get_page_data, format_ngo_email, get_test_data


def test():
    assert len(get_page_data()) >= 1


def test_formatting_email():
    assert format_ngo_email("info at dogrescuecenter.org") == "info@dogrescuecenter.org"


def test_getting_one_ngo():
    ngo = get_test_data()
    assert ngo["name"] == "Animal Sanctuary "
    assert ngo["country"] == "Thailand"
