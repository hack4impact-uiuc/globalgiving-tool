import mongomock

from globalgiving.commands.cmd_test import dev_testscraper


def test_scraper_not_found():
    # Mock collection - can only reliably test edge case
    # Scrapers may not always be present/start present
    mock_collection = mongomock.MongoClient().db.collection
    mock_collection.insert_one(dict(_id="url1", name="test1"))

    # Will not find viable scraper, should return None
    result = dev_testscraper(mock_collection, "test2")
    assert result is None
