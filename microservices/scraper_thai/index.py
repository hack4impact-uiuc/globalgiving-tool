from flask import Flask
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix
from src.scraper import basepage_scrape, get_one_ngo


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version="0.1", title="Thailand Scraper")


@api.route("/url")
class ScraperVietnam(Resource):
    def get(self):
        return "http://wiki.p2pfoundation.net/NGOs_in_Thailand"


@api.route("/data")
class ScraperVietnam(Resource):
    def get(self):
        orgs = basepage_scrape()
        return {"data": orgs}


@api.route("/test")
class ScraperVietnam(Resource):
    def get(self):
        org = get_one_ngo()
        return {"test": org}


if __name__ == "__main__":
    app.run(debug=True)
