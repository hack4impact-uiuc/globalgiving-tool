from app import app
from app.scraper import get_page_data, get_one_nonprofit
import json


@app.route("/routes")
def get_routes():
    return ["/data"]

@app.route("/test")
def test():
    return json.dumps(get_one_nonprofit(), indent=4, separators=(",", ": "))

@app.route("/data")
def page_data():
    return str(get_page_data())
