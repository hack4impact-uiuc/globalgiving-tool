import pymongo
import dotenv
import os
from globalgiving.s3_interface import init_s3_credentials
import json


def db_get_collection(collectionName="scrapers"):
    """
    Gets the scapers collection from the database. This function pulls the URI
    stored in an environment file. The purpose is simply to pass on the
    collection to other functions so they can do with it what they must.
    """
    if (os.path.isfile(os.getenv("HOME") + "/globalgiving/credentials.json"):
        with open(os.getenv("HOME") + "/globalgiving/credentials.json") as f:
            data = json.load(f)
        client = pymongo.MongoClient(data["mongo_uri"])
        db = client.get_database()
        collection = db[collectionName]
        return collection
    else:
        dotenv.load_dotenv(dotenv.find_dotenv())
        uri = os.getenv("URI")
        client = pymongo.MongoClient(uri)
        db = client.get_database()
        collection = db[collectionName]
        return collection


def send_scraper_to_db(name, url, namesList, routesList, test=False):
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
            delete_scraper(payload["_id"], test)
            post_id = scrapers.insert_one(payload).inserted_id
            updated = True
    return "Registration sent to db with id: " + post_id, updated


def list_scrapers_from_db(test=False):
    """
    Gets all scrapers listed in the database. This function merely returns the
    scrapers as a list.
    """
    if test:
        scrapers = db_get_collection("tests")
    else:
        scrapers = db_get_collection()
    cursor = scrapers.find({})
    document_list = [doc for doc in cursor]
    return document_list


def delete_scraper(scraper_id, test=False):
    if test:
        scrapers = db_get_collection("tests")
    else:
        scrapers = db_get_collection()
    return scrapers.delete_one({"_id": scraper_id})


def delete_all_scrapers(test=False):
    if test:
        scrapers = db_get_collection("tests")
        scrapers.delete_many({})
    else:
        pass  # Don't do anything if called by accident!


def upload_data(data, test=False):
    """
    Sends the NGO/CSO data to the database.
    Input:
        data: A list of dictionaries representing the NGOs.
    Returns:
        A confirmation that the data has been sent, otherwise an
        exception.
    """
    print(data)
    scrapers = db_get_collection("ngo_data")
    # bucket_name = name + "-" + str(hash(name))  # we need to figure out how
    # logging is going to work for uploading ngo data
    # payload[name] = bucket_name
    # client = init_s3_credentials()
    # client.create_bucket(Bucket=bucket_name)

    # purge duplicates
    data = purge_update_duplicates(data)
    if len(data) == 0:
        return "No new NGOs were found.\n\n"

    post_ids = scrapers.insert_many(data, ordered=False).inserted_ids
    try:
        assert len(data) == len(post_ids)
    except AssertionError:
        return "{} NGOs were duplicates or failed to upload. {} were successfully sent to the database.\n\n".format(
            len(data) - len(post_ids), len(post_ids)
        )
    return "Data for all {} NGOs sent to the database.\n\n".format(len(post_ids))


def list_ngos_from_db():
    """
    Get all NGOs currently in the database.
    """
    ngos = db_get_collection("ngo_data")
    cursor = ngos.find({})
    ngo_list = [doc for doc in cursor]
    for ngo in ngo_list:
        ngo["_id"] = str(ngo["_id"])
    return ngo_list


def purge_update_duplicates(ngos_to_upload):
    """
    Description:
        This function purges duplicate NGOs from a list of NGOs which need to
        be uploaded to a db, but it also should be able to detect when an NGO
        needs to be updated.
    Input:
        The list of NGOs to be uploaded
    Output:
        1) A list of NGOs which has been purged of duplicates
    """
    extant_ngos = str(list_ngos_from_db())

    new_ngos = []
    # use find to see if the name is already in the db
    # if it is, then check the url just to make sure
    for candidate_ngo in ngos_to_upload:
        if extant_ngos.find(candidate_ngo["name"]) == -1:
            new_ngos.append(candidate_ngo)
    return new_ngos
