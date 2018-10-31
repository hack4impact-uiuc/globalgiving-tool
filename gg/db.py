import pymongo
import json


def db_get_collection():
    username, password = "invalid", "invalid"
    with open('db-access.secret', 'r') as secretFile:
        username, password = [word.strip() for word in secretFile.readlines()]
    uri = "mongodb://{}:{}@ds147073.mlab.com:47073/ggdb-dev".format(username, password)
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    users_collection = db.users_collection
    return users_collection


def send_to_db(name, routes):
    users_collection = db_get_collection()
    payload = {"name": name, "routes": routes}
    post_id = users_collection.insert_one(payload).inserted_id
    return post_id


def list_from_db():
    users_collection = db_get_collection()
    cursor = users_collection.find({})
    document_list = [doc for doc in cursor]
    return document_list
