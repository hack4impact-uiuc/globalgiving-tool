import pymongo
import dotenv
import os


def db_get_collection():
    dotenv.load_dotenv(dotenv.find_dotenv())
    uri = os.getenv("URI")
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    scrapers = db.scrapers
    return scrapers


def send_to_db(name, url, namesList, routesList):
    scrapers = db_get_collection()
    payload = {"name": name}
    payload["_id"] = url
    routes = {}
    for routeName, routeURL in zip(namesList, routesList):
        routes[routeName] = routeURL
    payload["routes"] = routes
    try:
        post_id = scrapers.insert_one(payload).inserted_id
    except Exception as e:
        if type(e).__name__ == "DuplicateKeyError":
            return "Exception: DuplicateKeyError: Scraper with the same URL is already in the database."
    return "sent to db with id: " + post_id


def list_from_db():
    scrapers = db_get_collection()
    cursor = scrapers.find({})
    document_list = [doc for doc in cursor]
    return document_list
