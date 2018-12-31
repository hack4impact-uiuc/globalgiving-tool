import sys, os

sys.path.append(os.path.realpath(os.path.dirname(__file__) + "/.."))

from scraper import get_page_data


def test():
    assert len(get_page_data()) >= 1


test()
