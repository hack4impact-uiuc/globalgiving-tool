from app import app
from app.scraper import scrape, get_registration_site
import json


@app.route("/data")
def page_data():
    """Gets the relevant data from the page"""
    return scrape()

# WIP: should be able to take a country name and pass that to scraper function
@app.route("/registration")
def registration_site():
    return get_registration_site("australia")
    

@app.route("/routes")
def routes_available():
    """Returns a list of available routes to hit for this scraper."""
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )
