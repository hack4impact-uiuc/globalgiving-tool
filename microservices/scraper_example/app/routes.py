from app import app
from app.scraper import get_page_data
import json


@app.route("/")
def index():
    return "Hello, Python World!"


@app.route("/data")
def page_data():
    return str(get_page_data())


@app.route("/routes")
def routes_availible():
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )


"""Test Routes!"""


@app.route("/test1")
def test1():
    return "test1"
