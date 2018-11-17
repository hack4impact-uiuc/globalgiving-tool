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


@app.route("/test")
def test():
    return get_one_nonprofit()


@app.route("/data")
def page_data():
    return get_page_data()
