import pymongo
import dotenv
import os
from globalgiving.s3_interface import init_s3_credentials


def db_get_collection(collectionName="scrapers"):
    """
    Gets the scapers collection from the database. This function pulls the URI
    stored in an environment file. The purpose is simply to pass on the
    collection to other functions so they can do with it what they must.
    """
    dotenv.load_dotenv(dotenv.find_dotenv())
    uri = os.getenv("URI")
    client = pymongo.MongoClient(uri)
    db = client["ggdb-dev"]
    collection = db[collectionName]
    return collection


def send_to_db(name, url, namesList, routesList, test=False):
    """
    Sends the name and routes to the database.
    Input:
        name: the name of the scraper
        url: the base url of the scaper
        namesList: a list of the names of the various routes
        routesList: a list of the addresses of the various routes
    Returns:
        A confirmation that the scraper has been registered, otherwise an
        exception.
    """
    payload = {"name": name}
    payload["_id"] = url
    if test:
        scrapers = db_get_collection("tests")
    else:
        scrapers = db_get_collection()
        bucket_name = name + "-" + str(hash(name))
        payload[name] = bucket_name
        client = init_s3_credentials()
        client.create_bucket(Bucket=bucket_name)
    routes = {}
    for routeName, routeURL in zip(namesList, routesList):
        routes[routeName] = routeURL
    payload["routes"] = routes
    updated = False
    try:
        post_id = scrapers.insert_one(payload).inserted_id
    except Exception as e:
        if type(e).__name__ == "DuplicateKeyError":
            delete_ngo(payload["_id"])
            post_id = scrapers.insert_one(payload).inserted_id
            updated = True
    return "Registration sent to db with id: " + post_id, updated


def list_from_db(test=False):
    """
    Gets all scrapers listed in the database. This function merely returns the
    scrapers as a list. Printing and whatnot happens later.
    """
    if test:
        scrapers = db_get_collection("tests")
    else:
        scrapers = db_get_collection()
    cursor = scrapers.find({})
    document_list = [doc for doc in cursor]
    return document_list


def delete_ngo(ngo_id):
    scrapers = db_get_collection()
    return scrapers.delete_one({"_id": ngo_id})


def delete_all(test=False):
    if test:
        scrapers = db_get_collection("tests")
        scrapers.delete_many({})
    else:
        pass  # Don't do anything if called by accident!
