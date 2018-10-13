from flask import Flask
from scraper import basepage_scrape

app = Flask(__name__)


@app.route("/")
def my_first_route():
    basepage_scrape()
    return str(basepage_scrape())


if __name__ == "__main__":
    app.run(debug=True)
