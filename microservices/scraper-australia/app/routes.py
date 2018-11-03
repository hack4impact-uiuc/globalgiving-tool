from app import app
from app.scraper import get_page_data


@app.route("/routes")
def get_routes():
    return ["/data"]


@app.route("/data")
def page_data():
    return str(get_page_data())
