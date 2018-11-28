from app import app
from app.scraper import basepage_scrape
import json


@app.route("/data")
def page_data():
    return json.dumps(basepage_scrape(), indent=4, separators=(",", ": "))


<<<<<<< HEAD
=======
@app.route("/test")
def test():
    return json.dumps(get_one_ngo(), indent=4, separators=(",", ": "))


>>>>>>> cebd25ac9aa97f3dd1cee32993796ae26f29885e
@app.route("/routes")
def routes_availible():
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )
