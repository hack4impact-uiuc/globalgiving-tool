import click
import os, sys

from globalgiving.cli import pass_context
from globalgiving.db import (
    NGO_COLLECTION,
    db_get_collection,
    list_ngos_from_db,
    upload_data,
    delete_one_ngo_from_db,
)

SCRAPER_REG_PATH = "../../../microservices"  # Sibling package path
COUNTRY_FIELD = "country"
REGISTRATION_FIELD = "registration"

# Bring microservices directory into import path
sys.path.append(os.path.realpath(os.path.dirname(__file__) + SCRAPER_REG_PATH))
from scraper_registerids.src.scraper import get_registration_site, get_country_code


@click.command(
    "fill-ids",
    short_help="Enrich the database by finding and inserting an appropriate registration office url to documents without registration IDs",
)
@pass_context
def cli(ctx):
    """
    GG fill-ids enriches the database by inserting the site of the registration office for that specific country
    """
    # Specify collection to perform operations to
    collection = db_get_collection(NGO_COLLECTION)
    ctx.log("Finding and inserting registration office sites into the database...")

    # Get all ngos from the database that don't have a registration ID/site and have a country
    # to get registration office site
    ngo_list = list_ngos_from_db(collection, registration=None, country={"$ne": None})
    updated_list = []

    # Keep track of all countries seen so far to reduce amount of scraping
    prev_countries = dict()

    # Update the document to have a registration site, check edge case of no country, which can't be assigned
    # a registration site
    for org in ngo_list:
        # Check if country has been previously scraped already
        if org[COUNTRY_FIELD].title() in prev_countries.keys():
            org[REGISTRATION_FIELD] = [
                prev_countries[org[COUNTRY_FIELD]]
            ]  # Creates a list to easily add more registration IDs/fields
            updated_list.append(org)
        else:
            # Scrape for country code and add to dictionary
            registration_url = get_registration_site(org[COUNTRY_FIELD])
            prev_countries[org[COUNTRY_FIELD].title()] = registration_url
            org[REGISTRATION_FIELD] = [registration_url]
            updated_list.append(org)

    # Check list of updated NGOs and only delete/insert NGOs that now have registration office sites
    for updated_org in updated_list:
        if updated_org[REGISTRATION_FIELD][0] != "":
            delete_one_ngo_from_db(collection, _id=updated_org["_id"])

    # Push updated documents to database
    ctx.log(upload_data(collection, updated_list))
