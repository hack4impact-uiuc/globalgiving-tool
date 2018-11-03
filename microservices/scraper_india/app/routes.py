from app import app
from app.scraper import get_page_data
import json
from app.scraper import get_one_nonprofit


@app.route("/routes")
def routes_availible():
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )


@app.route("/test")
def test():
    return json.dumps(
        get_one_nonprofit(),
        indent=4,
        separators=(",", ": "),
    )



@app.route("/data")
def page_data():
    return str(get_page_data())
