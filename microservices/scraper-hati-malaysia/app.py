from flask import Flask
from scraper import scrape

app = Flask(__name__)


@app.route("/")
def my_first_route():
    return "<h1> no data </h1>"


@app.route("/data")
def page_data():
    return scrape()


if __name__ == "__main__":
    app.run(debug=True)
