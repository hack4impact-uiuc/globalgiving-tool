from flask import Flask
from scraper import basepage_scrape
from scraper import country_page_scrape

app = Flask(__name__)


@app.route("/scrape_all")
def scrape_all_ngos():
    return str(basepage_scrape())


@app.route("/colombia")
def scrape_colombia():
    return str(country_page_scrape("/colombia.html"))


@app.route("/routes")
def return_all_routes():
    return ["/scrape_all", ]


if __name__ == "__main__":
    app.run(debug=True)
