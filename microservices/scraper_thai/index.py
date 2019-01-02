from flask import Flask
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix
from src.scraper import get_page_data, get_test_data


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app)


@api.route("/url")
class Scraper(Resource):
    def get(self):
        return "http://wiki.p2pfoundation.net/NGOs_in_Thailand"


@api.route("/data")
class Scraper(Resource):
    def get(self):
        return {"data": get_page_data()}


@api.route("/test")
class Scraper(Resource):
    def get(self):
        return {"test": get_test_data()}


if __name__ == "__main__":
    app.run(debug=True)
