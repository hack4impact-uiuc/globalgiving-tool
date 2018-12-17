import dotenv
import boto3
import os
import json
import pymongo


def init_s3_credentials():

    with open(os.getenv("HOME") + "/globalgiving/credentials.json") as f:
        data = json.load(f)

        # print(os.getenv("HOME") + "/globalgiving/credentials.json")
        # print(data)
        # mongo_uri = os.getenv(data["mongo_uri"])
        # print(mongo_uri)
        client = pymongo.MongoClient(data["mongo_uri"])

        db = client.get_database()

        user_information = db["credentials"].find_one(
            {"mongo_uri": data["mongo_uri"], "token": data["token"]}
        )

        if user_information == None:
            print("Not authenticated")
            exit(0)

        access_key = user_information["access_key"]
        secret_key = user_information["secret_key"]

        client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            # aws_session_token=SESSION_TOKEN,
        )
        return client
