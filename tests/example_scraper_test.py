import unittest
from microservices.example_scraper import scraper

class TestExampleScraper(unittest.TestCase):

    def test_basic(self):
        self.assertTrue(scraper.get_page_data() is not None)

if __name__ == '__main__':
    unittest.main()