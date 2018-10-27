import pymongo


def send_to_db(name, routes):
    uri = "mongodb://aria:malkani28@ds139243.mlab.com:39243/gg-db"
    client = pymongo.MongoClient(uri)
    db = client.get_default_database()
    return db
