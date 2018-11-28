from app import app
from app.scraper import basepage_scrape, get_one_ngo
import json


@app.route("/data")
def page_data():
    return json.dumps(basepage_scrape(), indent=4, separators=(",", ": "))


@app.route("/test")
def test():
    return json.dumps(get_one_ngo(), indent=4, separators=(",", ": "))


@app.route("/routes")
def routes_availible():
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )
