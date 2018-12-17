from app import app
from app.scraper import scrape, get_registration_site
import json


@app.route("/data")
def page_data():
    """Gets the relevant data from the page"""
    return scrape()

@app.route("/registration/<country>")
def registration_site(country):
    return get_registration_site(country)
    

@app.route("/routes")
def routes_available():
    """Returns a list of available routes to hit for this scraper."""
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )
