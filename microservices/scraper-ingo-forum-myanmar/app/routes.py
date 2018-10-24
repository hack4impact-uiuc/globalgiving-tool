from app import app
from app.scraper import get_page_data
import json


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
