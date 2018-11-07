from app import app
from app.scraper import basepage_scrape, get_one_ngo
import json


@app.route("/data")
def page_data():
    return str(basepage_scrape())


@app.route("/test")
def test():
    return str(get_one_ngo())




@app.route("/routes")
def routes_availible():
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )
