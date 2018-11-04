from flask import Flask
from scraper import basepage_scrape
from scraper import country_page_scrape
import json

app = Flask(__name__)


@app.route("/scrape_all")
def scrape_all_ngos():
    return str(basepage_scrape())


@app.route("/colombia")
def scrape_colombia():
    return str(country_page_scrape("/colombia.html"))

@app.route("/ecuador")
def scrape_ecuador():
    return str(country_page_scrape("/ecuador.html"))

@app.route("/peru")
def scrape_peru():
    return str(country_page_scrape("/peru.html"))

@app.route("/bolivia")
def scrape_bolivia():
    return str(country_page_scrape("/bolivia.html"))

@app.route("/argentina")
def scrape_argentina():
    return str(country_page_scrape("/argentina.html"))

@app.route("/chile")
def scrape_chile():
    return str(country_page_scrape("/chile.html"))

@app.route("/brazil")
def scrape_brazili():
    return str(country_page_scrape("/brazili.html"))


@app.route("/routes")
def routes_available():
    """Returns a list of available routes to hit for this scraper."""
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )


if __name__ == "__main__":
    app.run(debug=True)
