from app import app
from app.scraper import scrape
import json


@app.route("/data")
def page_data():
    return scrape()


@app.rou
def routes_availible():
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )


@app.route("/url")
def url():
    return "http://www.hati.my/"


@app.route("/test")
def test():
    return scrape(one=True)  # switches to getting only one scraper
