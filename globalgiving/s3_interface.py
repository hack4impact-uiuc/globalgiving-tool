import dotenv
import boto3
import os


def init_s3_credentials():
    dotenv.load_dotenv(dotenv.find_dotenv())
    access_key = os.getenv("ACCESS_KEY")
    secret_key = os.getenv("SECRET_KEY")
    client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        # aws_session_token=SESSION_TOKEN,
    )
    return client
