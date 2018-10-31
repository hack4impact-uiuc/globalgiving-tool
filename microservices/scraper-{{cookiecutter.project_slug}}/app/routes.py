from app import app
from app.scraper import scrape
import json


@app.route("/data")
def page_data():
    """
    Gets the relevant data from the page
    """
    return


@app.route("/routes")
def routes_available():
    """
    Returns a list of available routes to hit for this scraper.
    """
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )
