import pymongo
import os
import dotenv
import requests
import pytest
from gg.db import send_to_db
from gg.db import list_from_db


def test_existence():
    name = "TEST"
    url = "https://gg-scraper-example.now.sh"
    namesList = ["Routes", "Test1", "Data", "Static"]
    routesList = [
        "https://gg-scraper-example.now.sh/routes",
        "https://gg-scraper-example.now.sh/test1",
        "https://gg-scraper-example.now.sh/data",
        "https://gg-scraper-example.now.sh/static/",
    ]
    status = send_to_db(name, url, namesList, routesList, test=True)
    assert (
        status == "Registration sent to db with id: https://gg-scraper-example.now.sh"
    )

    docs = list_from_db(test=True)
    assert len(docs) == 1

    name = docs[0]["Name"]
    assert name == "TEST"
