from flask import Flask
from scraper import scrape
import json

app = Flask(__name__)


@app.route("/data")
def page_data():
    return scrape()


@app.route("/routes")
def routes_availible():
    return json.dumps(
        ["%s" % rule for rule in app.url_map.iter_rules()],
        indent=4,
        separators=(",", ": "),
    )


if __name__ == "__main__":
    app.run(debug=True)
