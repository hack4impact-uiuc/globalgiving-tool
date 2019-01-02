from flask import Flask
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix
from src.scraper import get_page_data, get_one

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version="0.1", title="Uganda Scraper")


@api.route("/url")
class ScraperVietnam(Resource):
    def get(self):
        return "https://informationcradle.com/africa/list-of-ngos-in-uganda/"


@api.route("/data")
class ScraperVietnam(Resource):
    def get(self):
        orgs = get_page_data()
        return {"data": orgs}


@api.route("/test")
class ScraperVietnam(Resource):
    def get(self):
        org = get_one()
        return {"test": org}


if __name__ == "__main__":
    app.run(debug=True)
