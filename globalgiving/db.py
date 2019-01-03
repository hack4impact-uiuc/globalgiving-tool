import pymongo
import dotenv
import os
from globalgiving.s3_interface import init_s3_credentials
from globalgiving.config import (
    CREDENTIALS_PATH,
    CRED_URI_FIELD,
    NGO_COLLECTION,
    SCRAPER_COLL_NAME_FIELD,
)
import json


ENV_URI_FIELD = "URI"


def db_get_collection(collectionName="scrapers"):
    """
    Gets the scapers collection from the database. This function pulls the URI
    stored in an environment file. The purpose is simply to pass on the
    collection to other functions so they can do with it what they must.
    """
    if os.path.isfile(os.getenv("HOME") + CREDENTIALS_PATH):
        with open(os.getenv("HOME") + CREDENTIALS_PATH) as f:
            data = json.load(f)
        client = pymongo.MongoClient(data[CRED_URI_FIELD])
        db = client.get_database()
        collection = db[collectionName]
        return collection
    else:
        dotenv.load_dotenv(dotenv.find_dotenv())
        uri = os.getenv(ENV_URI_FIELD)
        client = pymongo.MongoClient(uri)
        db = client.get_database()
        collection = db[collectionName]
        return collection


def send_scraper_to_db(collection, name, url, test=False):
    """
    Sends the name and routes to the database.
    Input:
        collection: collection to send the scraper to
        name: the name of the scraper
        url: the base url of the scaper
        namesList: a list of the names of the various routes
        routesList: a list of the addresses of the various routes
    Returns:
        A confirmation that the scraper has been registered, otherwise an
        exception.
    """
    payload = {SCRAPER_COLL_NAME_FIELD: name}
    payload["_id"] = url

    if not test:
        # only run code if not testing to prevent continuous creation of s3 buckets
        bucket_name = name + "-" + str(hash(name))
        payload[name] = bucket_name
        client = init_s3_credentials()
        client.create_bucket(Bucket=bucket_name)

    updated = False
    try:
        post_id = collection.insert_one(payload).inserted_id
    except Exception as e:
        if type(e).__name__ == "DuplicateKeyError":
            delete_scraper(collection, payload["_id"])
            post_id = collection.insert_one(payload).inserted_id
            updated = True
        else:
            print(e)
            return
    return "Registration sent to db with id: " + post_id, updated


def list_scrapers_from_db(collection):
    """
    Gets all scrapers listed in the database in the specified collection. This function merely returns the
    scrapers as a list.
    """
    cursor = collection.find({})
    document_list = [doc for doc in cursor]
    return document_list


def delete_scraper(collection, scraper_id):
    return collection.delete_one({"_id": scraper_id})


def upload_data(collection, data):
    """
    Sends the NGO/CSO data to the database.
    Input:
        data: A list of dictionaries representing the NGOs.
    Returns:
        A confirmation that the data has been sent, otherwise an
        exception.
    """
    # purge duplicates
    data = data["data"]
    data = purge_update_duplicates(collection, data)
    if len(data) == 0:
        return "No new NGOs were found.\n\n"
    post_ids = collection.insert_many(data, ordered=False).inserted_ids
    try:
        assert len(data) == len(post_ids)
    except AssertionError:
        return "{} NGOs were duplicates or failed to upload. {} were successfully sent to the database.\n\n".format(
            len(data) - len(post_ids), len(post_ids)
        )
    return "Data for all {} NGOs sent to the database.\n\n".format(len(post_ids))


def list_ngos_from_db(collection, **kwargs):
    """
    Get all NGOs currently in the database with the option of passing in query parameters.

    Input:
        collection: collection to get NGO data from
        kwargs: used to specify query parameters
    """
    cursor = collection.find(kwargs)
    ngo_list = [doc for doc in cursor]
    for ngo in ngo_list:
        ngo["_id"] = str(ngo["_id"])
    return ngo_list


def delete_one_ngo_from_db(collection, **kwargs):
    """
    Delete ngos in the database with the option of passing in query parameters

    Input:
        collection: collection to get NGO data from
        kwargs: used to specify query parameters
    """
    collection.delete_one(kwargs)


def purge_update_duplicates(collection, ngos_to_upload):
    """
    Description:
        This function purges duplicate NGOs from a list of NGOs which need to
        be uploaded to a db, but it also should be able to detect when an NGO
        needs to be updated.
    Input:
        The collection to upload into
        The list of NGOs to be uploaded
    Output:
        1) A list of NGOs which has been purged of duplicates
    """
    extant_ngos = str(list_ngos_from_db(collection))

    new_ngos = []
    # use find to see if the name is already in the db
    # if it is, then check the url just to make sure
    for candidate_ngo in ngos_to_upload:
        if extant_ngos.find(candidate_ngo["name"]) == -1:
            new_ngos.append(candidate_ngo)
    return new_ngos
