from flask import Flask
from flask_restplus import Resource, Api, fields
from werkzeug.contrib.fixers import ProxyFix
from src.scraper import scrape, scrape_page

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version="0.1", title="Vietnam Scraper")


@api.route("/url")
class ScraperVietnam(Resource):
    def get(self):
        return "http://www.hati.my/"


@api.route("/data")
class ScraperVietnam(Resource):
    def get(self):
        orgs = scrape()
        return {"pages": orgs["pages"]}

# http://www.hati.my/education/kaseh-class/

@api.route("/page/<number>")
class ScraperVietnam(Resource):
    def get(self, number):
        links = scrape()
        orgs = scrape_page(links["urls"][int(number)])
        return {"data": orgs}

@api.route("/test")
class ScraperVietnam(Resource):
    def get(self):
        org = scrape(one=True)
        return {"test": org}


if __name__ == "__main__":
    app.run(debug=True)
