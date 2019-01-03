import mongomock

from globalgiving.commands.cmd_list import dev_list


def test_list_no_scrapers():
    # Mock collection
    mock_collection = mongomock.MongoClient().db.collection

    result = dev_list(mock_collection)
    assert len(result) == 0


def test_list_scrapers():
    # Mock collection
    mock_collection = mongomock.MongoClient().db.collection
    mock_collection.insert_one(dict(_id="url1", name="test1"))
    assert mock_collection.count_documents({}) == 1

    result = dev_list(mock_collection)
    assert len(result) == 1