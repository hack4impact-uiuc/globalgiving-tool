import click
import mongomock

from globalgiving.commands.cmd_crawled import dev_crawled


def test_crawled_no_links():
    # Test that the crawler returns a set of results - difficult to consistently test a specific result
    # Mock collection
    mock_collection = mongomock.MongoClient().db.collection

    # Test return string of function when no links in database
    result = dev_crawled(mock_collection)
    assert not result # In the actual function it will print a description followed by no results
    assert len(result) == 0


def test_crawled_present_links():
    # Mock collection and insert test objects
    mock_collection = mongomock.MongoClient().db.collection
    objects = [
        dict(url="test1", num_phone_numbers=100, num_addresses=0, num_subpages=0, num_word_ngo=0, composite_score=100),
        dict(url="test2", num_phone_numbers=0, num_addresses=100, num_subpages=0, num_word_ngo=0, composite_score=100)
    ] # Currently the composite score is being calculated by adding the remaining numbers, this test will fail if that calculation changes
    mock_collection.insert_many(objects)
    assert mock_collection.count_documents({}) == 2

    # Test command, results is a list of tuples
    result = dev_crawled(mock_collection)
    assert len(result) == 2
    assert result[0][0] == "test1"
    assert result[0][1] == 100
