from flask import Flask
from scraper import get_page_data

app = Flask(__name__)


@app.route("/run")
def scrape():
    return get_page_data()


@app.route("/route")
def get_routes():
    return [app.url_map]


if __name__ == "__main__":
    app.run(debug=True)
