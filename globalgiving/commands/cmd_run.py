import click, requests

import hashlib
import os
import uuid
from globalgiving.config import NGO_COLLECTION, SCRAPER_COLL_NAME_FIELD
from globalgiving.db import db_get_collection, list_scrapers_from_db, upload_data
from globalgiving.cli import pass_context, authenticate
from globalgiving.s3_interface import init_s3_credentials
import json


@click.command("run", short_help="Run a scraper")
@click.argument("n", required=False)
@click.option("-a", is_flag=True)
@pass_context
def cli(ctx, n, a):
    authenticate()
    collection = db_get_collection()
    ngo_collection = db_get_collection(NGO_COLLECTION)
    client = init_s3_credentials()

    if a:
        run_all(ctx)
        return

    # Create new bucket name for log file by using hash
    h = hashlib.md5()
    h.update(n.encode("utf-8"))
    bucket_name = n + "-" + h.hexdigest()

    # Generate unique file name for new log
    filename = str(uuid.uuid4()) + ".txt"
    f = open(filename, "w+")

    search = "Finding scraper {} from list of registered scrapers..."
    f.write(search.format(n) + "\n")
    try:
        scrapers = list_scrapers_from_db(collection)
        route_data = list(
            filter(lambda scraper: scraper[SCRAPER_COLL_NAME_FIELD] == str(n), scrapers)
        )
        if len(route_data) == 0:
            print("Scraper not found")
            return
        route_data = route_data[0]
        route = route_data["_id"] + "/data"
        f.write("Scraper {} found!".format(n) + "\n")
    except StopIteration:
        f.write("Scraper {} not found!".format(n) + "\n")
        f.close()
        client.upload_file(filename, bucket_name, filename)
        os.remove(filename)
        return
    try:
        # Run scraper by getting the correct route and requesting it
        contents = requests.get(route).json()
        if "data" in contents:
            print("The data is uploaded")
            f.write(upload_data(contents))
        elif "pages" in contents:
            print("Fetching all " + str(contents["pages"]) + " pages")
            f.write("Fetching all " + str(contents["pages"]) + " pages")
            for i in range(int(contents["pages"])):
                try:
                    url = str(route_data["_id"]) + "page"
                    # TODO: Current hack-run the scraper on localhost, and it will get all the pages, there is a deployment bug atm
                    url = "http://localhost:5000/page"
                    print("Fetching " + url)
                    f.write("Fetching " + url)
                    # contents = requests.get(route).json()
                    payload = {"url": str(contents["urls"][i])}
                    print(payload)
                    data = requests.post(url, json=json.dumps(payload))
                    print(data.json())
                    f.write(upload_data(data.json()))
                    print("The data is uploaded")
                except Exception as e:
                    print(e)
                    f.write("Failed on page" + str(route))
                    continue
        else:
            print("The data recieved is not structured correctly")
            f.write("The data recieved is not structured correctly")
    except Exception as e:
        print("exception")
        print(e)
        contents = str(e) + "\nFAILED"
        f.write(contents)

    f.close()

    # Call S3 to list current buckets
    response = client.list_buckets()

    # Get a list of all bucket names from the response
    buckets = [bucket["Name"] for bucket in response["Buckets"]]

    if bucket_name not in buckets:
        client.create_bucket(Bucket=bucket_name)

    client.upload_file(filename, bucket_name, filename)

    os.remove(filename)
    ctx.log("Wrote logs to file: " + filename)


def run_all(ctx):
    authenticate()
    collection = db_get_collection()
    ngo_collection = db_get_collection(NGO_COLLECTION)
    client = init_s3_credentials()

    h = hashlib.md5()
    names = []
    routes = []
    log_files = []
    log_filenames = []

    try:
        scrapers = list_scrapers_from_db(collection)
        for scraper in scrapers:
            n = scraper[SCRAPER_COLL_NAME_FIELD]
            names.append(n)
            routes.append(scraper["_id"] + "/data")
            h.update(n.encode("utf-8"))
            bucket_name = n + "-" + h.hexdigest()
            filename = str(uuid.uuid4()) + ".txt"
            log_filenames.append(filename)
            log_files.append(open(filename, "w+"))
    except Exception as e:
        n = "all"  # the name in this case is effectively all, then we can just
        # use the code from the single case
        h.update(n.encode("utf-8"))
        bucket_name = n + "-" + h.hexdigest()
        filename = str(uuid.uuid4()) + ".txt"
        f = open(filename, "w+")
        f.write("Scraper not found!" + "\n")
        f.write(str(e) + "\nFAILED")
        f.close()
        client.upload_file(filename, bucket_name, filename)
        os.remove(filename)
        ctx.log("Failed. See log at {} in bucket {}.".format(filename, bucket_name))
        return

    # Call S3 to list current buckets to prepare for logging
    response = client.list_buckets()
    # Get a list of all bucket names from the response
    buckets = [bucket["Name"] for bucket in response["Buckets"]]

    for name, route, log, filename in zip(names, routes, log_files, log_filenames):
        try:
            ctx.log("Getting information for {} . . . ".format(name))
            contents = requests.get(route)
            log.write(contents.text)
            log.write(upload_data(ngo_collection, json.loads(contents.text)))
            log.write("Upload succeeded!")
            ctx.log("Uploading {} succeeded!".format(name))
        except Exception as e:
            log.write("Upload failed.")
            ctx.log("Uploading {} failed.".format(name))
        finally:
            log.close()

        if bucket_name not in buckets:
            client.create_bucket(Bucket=bucket_name)

        client.upload_file(filename, bucket_name, filename)
        os.remove(filename)
        ctx.log("Wrote logs for {} to file: ".format(name) + filename)
