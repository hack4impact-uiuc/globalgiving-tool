from app import app
from app.scraper import get_page_data, get_one_nonprofit
import json


@app.route("/routes")
def routes_availible():
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )


@app.route("/url")
def url():
    return "http://www.findouter.com/Oceania/Australia/Society-and-Culture/Non-Governmental-Organisations/"


@app.route("/test")
def test():
    print(get_one_nonprofit())
    return json.dumps(get_one_nonprofit(), indent=4, separators=(",", ": "))


@app.route("/data")
def page_data():
    return get_page_data()
