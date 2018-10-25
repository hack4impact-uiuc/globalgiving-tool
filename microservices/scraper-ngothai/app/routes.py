# from flask import Flask
# from app.scraper import basepage_scrape

# app = Flask(__name__)


# @app.route("/scrape_all")
# def scrape_all_thai_ngos():
#     # return str(basepage_scrape())
#     return "Hello world!"


# @app.route("/routes")
# def return_all_routes():
#     return ["/scrape_all"]


# if __name__ == "__main__":
#     app.run(debug=True)

from app import app
from app.scraper import basepage_scrape
import json


@app.route("/data")
def page_data():
    return str(basepage_scrape())


@app.route("/routes")
def routes_availible():
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )
