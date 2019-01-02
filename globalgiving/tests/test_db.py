import mongomock
import pytest
from globalgiving.db import (
    send_scraper_to_db,
    list_scrapers_from_db,
)

# import pymongo
# import os
# import dotenv
# import requests


def test_existence():
    # Mock collection
    mock_collection = mongomock.MongoClient().db.collection

    # # Clear the testing collection
    # delete_all_scrapers(test=True)

    name = "test"
    url = "https://gg-scraper-example.now.sh"
    namesList = ["Routes", "Test1", "Data", "Static"]
    routesList = [url + "/" + name.lower() for name in namesList]
    routesList[-1] += "/"  # last route is always static which has another /
    status = send_scraper_to_db(mock_collection, name, url, namesList, routesList)[
        0
    ]  # Send to db returns as tuple
    assert (
        status == "Registration sent to db with id: https://gg-scraper-example.now.sh"
    )

    docs = list_scrapers_from_db(mock_collection)
    assert len(docs) == 1

    name = docs[0]["name"]
    # print(name)
    assert name == "test"

    static_route = docs[0]["routes"]["Static"]
    assert static_route == "https://gg-scraper-example.now.sh/static/"


def test_update():
    # Mock collection
    mock_collection = mongomock.MongoClient().db.collection

    # # Clear the testing collection
    # delete_all_scrapers(test=True)

    name = "test"
    url = "https://gg-scraper-example.now.sh"
    # create a fake routes called Test1
    namesList = ["Routes", "Test1", "Data", "Static"]
    routesList = [url + "/" + name.lower() for name in namesList]
    routesList[-1] += "/"  # last route is always static which has another /
    status = send_scraper_to_db(mock_collection, name, url, namesList, routesList)[0]
    assert (
        status == "Registration sent to db with id: https://gg-scraper-example.now.sh"
    )

    status = send_scraper_to_db(mock_collection, name, url, namesList, routesList)[0]
    assert (
        status == "Registration sent to db with id: https://gg-scraper-example.now.sh"
    )
