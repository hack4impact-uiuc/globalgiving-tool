from flask import Flask
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix
from src.scraper import get_one_nonprofit, get_page_data

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app)


@api.route("/url")
class Scraper(Resource):
    def get(self):
        return "https://ngosindia.com/ngos-of-india/"s


@api.route("/data")
class Scraper(Resource):
    def get(self):
        return {"data": get_one_nonprofit()}


@api.route("/test")
class Scraper(Resource):
    def get(self):
        return {"test": get_test_data()}


if __name__ == "__main__":
    app.run(debug=True)
