from flask import Flask
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix
from src.scraper import get_test_data, get_page_data

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version="0.1", title="Vietnam Scraper")


@api.route("/url")
class ScraperVietnam(Resource):
    def get(self):
        return {"url": "https://www.viet.net/community/nonprofit/"}


@api.route("/data")
class ScraperVietnam(Resource):
    def get(self):
        orgs = get_page_data()
        return {"data": orgs}


@api.route("/test")
class ScraperVietnam(Resource):
    def get(self):
        orgs = get_test_data()
        return {"test": str(orgs[0])}


if __name__ == "__main__":
    app.run(debug=True)
