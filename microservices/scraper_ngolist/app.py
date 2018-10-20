from flask import Flask
from scraper import basepage_scrape

app = Flask(__name__)


@app.route("/scrape_all")
def scrape_all_ngos():
    return str(basepage_scrape())


@app.route("/routes")
def return_all_routes():
    return ["/scrape_all"]


if __name__ == "__main__":
    app.run(debug=True)
