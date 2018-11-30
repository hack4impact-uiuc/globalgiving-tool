from app import app
from app.scraper import get_page_data,get_test_data
import json


@app.route("/")
def index():
    return "Hello, Python World!"


@app.route("/data")
def page_data():
    orgs = get_page_data()
    print(orgs[0:2])
    return str(orgs)


@app.route("/routes")
def routes_availible():
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )


"""Test Routes!"""


@app.route("/test")
def test():
    orgs = get_test_data()
    return str(orgs[0])
