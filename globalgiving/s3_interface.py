import dotenv
import boto3
import os
import json
import pymongo
from globalgiving.config import (
    CREDENTIALS_PATH,
    CRED_URI_FIELD,
    CRED_TOKEN_FIELD,
    CRED_ACCESS_FIELD,
    CRED_SECRET_FIELD,
)


def init_s3_credentials():

    with open(os.getenv("HOME") + CREDENTIALS_PATH) as f:
        data = json.load(f)

        # print(os.getenv("HOME") + "/globalgiving/credentials.json")
        # print(data)
        # mongo_uri = os.getenv(data["mongo_uri"])
        # print(mongo_uri)
        client = pymongo.MongoClient(data[CRED_URI_FIELD])

        db = client.get_database()

        user_information = db["credentials"].find_one(
            {
                CRED_URI_FIELD: data[CRED_URI_FIELD],
                CRED_TOKEN_FIELD: data[CRED_TOKEN_FIELD],
            }
        )

        if user_information == None:
            print("Not authenticated")
            exit(0)

        access_key = user_information[CRED_ACCESS_FIELD]
        secret_key = user_information[CRED_SECRET_FIELD]

        client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            # aws_session_token=SESSION_TOKEN,
        )
        return client
