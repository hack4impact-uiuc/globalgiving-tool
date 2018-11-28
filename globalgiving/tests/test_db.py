import pymongo
import os
import dotenv
import requests
import pytest
from globalgiving.db import send_to_db, list_from_db, delete_all


def test_existence():
    # Clear the testing collection
    delete_all(test=True)

    name = "TEST"
    url = "https://gg-scraper-example.now.sh"
    namesList = ["Routes", "Test1", "Data", "Static"]
    routesList = [url + "/" + name.lower() for name in namesList]
    routesList[-1] += "/"  # last route is always static which has another /
    status = send_to_db(name, url, namesList, routesList, test=True)
    # assert (
    #     status == "Registration sent to db with id: https://gg-scraper-example.now.sh"
    # )

    docs = list_from_db(test=True)
    # assert len(docs) == 1

    name = docs[0]["name"]
    # assert name == "TEST"

    static_route = docs[0]["routes"]["Static"]
    # assert static_route == "https://gg-scraper-example.now.sh/static/"


def test_rejection():
    # Clear the testing collection
    delete_all(test=True)

    name = "TEST"
    url = "https://gg-scraper-example.now.sh"
    # create a fake routes called Test1
    namesList = ["Routes", "Test1", "Data", "Static"]
    routesList = [url + "/" + name.lower() for name in namesList]
    routesList[-1] += "/"  # last route is always static which has another /
    status = send_to_db(name, url, namesList, routesList, test=True)
    # assert (
    #     status == "Registration sent to db with id: https://gg-scraper-example.now.sh"
    # )

    status = send_to_db(name, url, namesList, routesList, test=True)
    # assert (
    #     status
    #     == "Exception: DuplicateKeyError: Scraper with the same URL is already in the database."
    # )
