import mongomock
import pytest
from globalgiving.db import send_scraper_to_db, list_scrapers_from_db


def test_existence():
    # Mock collection and test data
    mock_collection = mongomock.MongoClient().db.collection
    name = "test"
    url = "url1"

    send_scraper_to_db(mock_collection, name, url, test=True)
    assert mock_collection.count_documents({}) == 1

    docs = list_scrapers_from_db(mock_collection)
    assert docs[0]["name"] == "test"
    assert docs[0]["_id"] == "url1"


def test_update():
    # Mock collection and test data
    mock_collection = mongomock.MongoClient().db.collection
    mock_collection.insert_one(dict(_id="url1", name="test"))
    name = "test"
    url = "url1"

    status = send_scraper_to_db(mock_collection, name, url, test=True)[0]
    assert status == "Registration sent to db with id: url1"
    assert mock_collection.count_documents({}) == 1

    docs = list_scrapers_from_db(mock_collection)
    assert docs[0]["name"] == "test"
    assert docs[0]["_id"] == "url1"
