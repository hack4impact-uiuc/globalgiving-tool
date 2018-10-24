from flask import Flask
from scraper import get_page_data

app = Flask(__name__)


@app.route("/data")
def page_data():
    return str(get_page_data())


@app.route("/routes")
def routes_availible():
    return ",\n".join(["%s" % rule for rule in app.url_map.iter_rules()])


if __name__ == "__main__":
    app.run(debug=True)
