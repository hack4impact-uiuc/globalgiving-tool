import mongomock

from globalgiving.commands.cmd_crawl import dev_crawl

TEST_COUNTRY = "argentina"


def test_crawl_results_exist():
    # Test that the crawler returns a set of results - difficult to consistently test a specific result
    # Mock collection
    mock_collection = mongomock.MongoClient().db.collection

    # Call test crawl and push data to mock database
    dev_crawl(mock_collection, TEST_COUNTRY)

    # Get results and test
    cursor = mock_collection.find({})
    results = [doc for doc in cursor]
    assert results is not None
    assert len(results) >= 1
