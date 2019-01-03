import click
import mongomock

from globalgiving.commands.cmd_delete import dev_delete


def test_delete_not_found():
    # Test that the crawler returns a set of results - difficult to consistently test a specific result
    # Mock collection
    mock_collection = mongomock.MongoClient().db.collection
    mock_collection.insert_one(dict(_id="test1", name="scraper1"))
    assert mock_collection.count_documents({}) == 1

    # Test delete on not present scraper
    dev_delete(mock_collection, "test2")
    assert mock_collection.count_documents({}) == 1


def test_delete_found():
    # Test that the crawler returns a set of results - difficult to consistently test a specific result
    # Mock collection
    mock_collection = mongomock.MongoClient().db.collection
    objects = [dict(_id="test1", name="scraper1"), dict(_id="test2", name="scraper2")]
    mock_collection.insert_many(objects)
    assert mock_collection.count_documents({}) == 2

    # Test delete on present scraper
    dev_delete(mock_collection, "scraper1")
    assert mock_collection.count_documents({}) == 1
