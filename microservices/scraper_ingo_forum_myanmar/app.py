from flask import Flask
from scraper_ingo_forum_myanmar.app.scraper import get_page_data

app = Flask(__name__)


@app.route("/routes")
def get_routes():
    return ["/run"]


@app.route("/run")
def scrape():
    return str(get_page_data())


if __name__ == "__main__":
    app.run(debug=True)
